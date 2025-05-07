    
    def compute_assignment_costs(self, current_time):
        # Environmental cost: C(i)
        env_cost = { 
            vm_idx :
            self.objective(current_time, vm_obj)
            for vm_idx, vm_obj in self.vm_instances.items()

        }
        return env_cost


    def estimate_migration_cost(self, job, src_vm, dst_vm):
        # Placeholder for actual migration cost logic
        return 1 # to prevent useless migrations



    def compute_migration_costs(self, J_q, J_r):
        # Migration cost: M(j,i)
        migr_cost = {
            (j_idx, vm_idx): 0
            if j_idx in J_q or (j_idx in J_r and vm_idx == self.running_jobs[j_idx][1])
            else self.estimate_migration_cost(self.running_jobs[j_idx][0] , self.running_jobs[j_idx][1], vm_idx)
            for j_idx in J_q + J_r
            for vm_idx in self.vm_instances.keys()
        }
        return migr_cost

    def step_schedule_MILP(self, t: datetime, J_q: list, J_r: list) -> dict: 

        C = self.compute_assignment_costs(t)
        M = self.compute_migration_costs(J_q, J_r)

        J_all = J_q + J_r
        V_all = self.vm_instances.keys()

        model = pulp.LpProblem("HourlySchedulingWithMigration", pulp.LpMinimize)
        x = pulp.LpVariable.dicts("x", ((j, i) for j in J_all for i in V_all), cat='Binary')

        # Objective
        model += pulp.lpSum(
            x[j, i] * (C[i] + M[(j, i)]) for j in J_all for i in V_all
        )

        # Constraints
        for j in J_all:
            model += pulp.lpSum(x[j, i] for i in V_all) == 1

        for i in V_all:
            model += pulp.lpSum(x[j, i] for j in J_all) <= 1

        model.solve(pulp.GUROBI(msg=True))

        return self.extract_step_output(x, J_all, V_all)



    def extract_step_output_MILP(self, x, J_all, V_all):
        assignment = {
            j : [i  for i in V_all if pulp.value(x[j, i]) == 1][0]
            for j in J_all
            
        }
        return assignment



    def run_simulation_MILP(self):    
        current_time = config.dt_i
        end_time = config.dt_f
        timestamps = utils.get_timestamps(config.dt_i, config.dt_f, config.step)
        footprints = {
            (dc.provider, dc.location): {
                t: {
                    "carbon": .0,
                    "water": .0,
                    "land_use": .0
                }
                for t in timestamps
            }    
            for dc in self.datacenters.values() 
        }

        out_str = f"Simulation from {current_time} to {end_time} with step {config.step}.\n"
        out_str += f"Jobs: {len(self.jobs)}\n"
        out_str += f"VMs: {len(self.vm_instances)}\n"
        out_str += str([(j_idx, job.lifetime) for j_idx, job in self.jobs.items()])
        out_str += "__________________________________________\n"
        while current_time < end_time:
            out_str += f"Current time: {current_time}\n"
            # get jobs in queue and running jobs
            J_q = self.get_job_queue_at_time(current_time)
            J_r = self.get_running_jobs()
            assignment = self.step_schedule(current_time, J_q, J_r)
            
            # update vm availability
            for vm_idx, vm_obj in self.vm_instances.items():
                if vm_idx in assignment.values():
                    vm_obj.available = False
                else:
                    vm_obj.available = True
            # update running jobs
            for j_idx, job in self.jobs.items():
                if j_idx in assignment.keys():
                    self.running_jobs[j_idx] = (job, assignment[j_idx])
            
        
            out_str += f"Assignments at {current_time}: {assignment}\n"
            

            # advance running time
            to_del_rj = []
            for j_idx, (job, vm_idx) in self.running_jobs.items(): 
                vm = self.vm_instances[vm_idx]
                # update footprints
                percentage_of_step = min(1, job.lifetime/config.step.seconds) 
                footprints[(vm.datacenter.provider, vm.datacenter.location)][current_time]["carbon"] += models.objectives.compute_carbon_at_time(current_time, vm) * percentage_of_step
                footprints[(vm.datacenter.provider, vm.datacenter.location)][current_time]["water"] += models.objectives.compute_water_at_time(current_time, vm) * percentage_of_step
                footprints[(vm.datacenter.provider, vm.datacenter.location)][current_time]["land_use"] += models.objectives.compute_land_use_at_time(current_time, vm) * percentage_of_step
                out_str += f"\tjob {j_idx} lifetime {job.lifetime}, percentage of step remaining {percentage_of_step}\n"
                # udate job lifetime
                job.lifetime -= config.step.seconds
                # remove completed jobs and release VMs
                if job.lifetime <= 0:
                    vm.available = True
                    to_del_rj.append(j_idx)
                    out_str += f"Job {j_idx} completed and VM {vm_idx} released.\n"
                    
                
            for j_idx in to_del_rj:
                del self.running_jobs[j_idx]
            out_str += "__________________________________________\n"
            current_time += config.step
        return footprints, out_str