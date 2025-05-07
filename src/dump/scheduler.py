import pulp
class Scheduler:
    def __init__(self, jobs, datacenters, vm_instances):#vm_indices_mapping, max_vm):
        self.jobs = jobs
        self.datacenters = datacenters
        self.vm_instances = vm_instances
        #self.vm_indices_mapping = vm_indices_mapping
        #self.max_vm = max_vm


    def schedule(self):
        pass

    def precompute_scheduling_costs(self, objective):
        env_cost = {
            (job_idx, vm_idx): 
                
                objective(vm_obj.datacenter.get_trace_footprints(
                    timestamp=job.release_time, 
                    runtime=job.runtime, 
                    vm_instance=vm_obj)
                ) 
            for job_idx, job in self.jobs.items()
            for vm_idx, vm_obj in self.vm_instances.items()
        }
    
        return env_cost
    
    def MILP_schedule(self, obj_eval):
        
        env_cost = self.precompute_scheduling_costs(obj_eval)

        J = list(self.jobs.keys())  # Jobs
        VM = list(self.vm_instances.keys())  # VM instances

        # --- PuLP Model ---
        model = pulp.LpProblem("GreenJobScheduling", pulp.LpMinimize)

        # Decision variables
        x = pulp.LpVariable.dicts("x", ((j, i) for j in J for i in VM), cat='Binary')

        # Objective
        model += pulp.lpSum(x[j, i] * env_cost[(j, i)] for j in J for i in VM)
        
        # Constraint: each job assigned to exactly one VM
        for j in J:
            model += pulp.lpSum(x[j, i] for i in VM) == 1

        # Constraint: each vm assigned to at most one job
        for i in VM:
            model += pulp.lpSum(x[j, i] for j in J) <= 1

        # Solve
        model.solve(pulp.GUROBI(msg=True))

        return self.extract_output(x)
    
    def extract_output(self, x):
        # --- Output results ---
        footprints = {
            (dc.provider, dc.location): [] for dc in self.datacenters.values()
        }

        for j, job in self.jobs.items() :
            for i, vm in self.vm_instances.items():
                if pulp.value(x[j, i]) == 1:
                    #print(f"Job {j} assigned to VM {i} in DC {n}")
                    dc = vm.datacenter
                    footprints[(dc.provider, dc.location)].append(
                        dc.get_trace_footprints(
                            timestamp=job.release_time,
                            runtime=job.runtime,
                            vm_instance=vm
                        )

                    )
        return footprints
    

    """
    def precompute_scheduling_costs(self, objective):
        env_cost = {
            (job_idx, dc_idx, vm_idx): 
                objective(dc.get_trace_footprints(
                    timestamp=job.release_time, 
                    n_nodes=1, 
                    runtime=job.runtime, 
                    vm_instance_name=vm_name)
                ) if self.max_vm[(dc_idx, vm_idx)]>.0 else float("inf")
            for job_idx, job in self.jobs.items()
            for dc_idx, dc in self.datacenters.items()
            for vm_idx, vm_name in self.vm_indices_mapping.items()
        }
    
        return env_cost
    

    def MILP_schedule(self, obj_eval):
        
        env_cost = self.precompute_scheduling_costs(obj_eval)

        J = list(self.jobs.keys())  # Jobs
        D = list(self.datacenters.keys())  # Datacenters
        VM = list(self.vm_indices_mapping.keys())  # VM instances

        # --- PuLP Model ---
        model = pulp.LpProblem("GreenJobScheduling", pulp.LpMinimize)

        # Decision variables
        x = pulp.LpVariable.dicts("x", ((j, n, i) for j in J for n in D for i in VM), cat='Binary')

        # Objective
        model += pulp.lpSum(x[j, n, i] * env_cost[(j, n, i)] for j in J for n in D for i in VM if env_cost[(j, n, i)] != float("inf") )

        # Constraint: each job assigned to exactly one VM
        for j in J:
            model += pulp.lpSum(x[j, n, i] for n in D for i in VM) == 1

        # Capacity constraint
        for n in D:
            for i in VM:
                model += pulp.lpSum(x[j, n, i] for j in J) <= self.max_vm[(n, i)]

        # Solve
        model.solve(pulp.GUROBI(msg=True))

        return self.extract_output(x)

    def extract_output(self, x):
        # --- Output results ---
        footprints = {
            (dc.provider, dc.location): [] for dc in self.datacenters.values()
        }

        for j in list(self.jobs.keys()) :
            for n in list(self.datacenters.keys()):
                for i in list(self.vm_indices_mapping.keys()):
                    if pulp.value(x[j, n, i]) == 1:
                        #print(f"Job {j} assigned to VM {i} in DC {n}")
                        
                        footprints[(self.datacenters[n].provider, self.datacenters[n].location)].append(
                            self.datacenters[n].get_trace_footprints(
                                timestamp=self.jobs[j].release_time,
                                n_nodes=1,
                                runtime=self.jobs[j].runtime,
                                vm_instance_name=self.vm_indices_mapping[i]
                            )

                        )
        return footprints
    """
    def geo_baseline_schedule(self):
        footprints = {
            (dc.provider, dc.location): [] for dc in self.datacenters.values()
        }
        dc_mapping = {
            (dc.provider, dc.location): dc for dc in self.datacenters.values()
        }
        
        
        for job_idx, job in self.jobs.items():

            dc = dc_mapping[(job.release_platform, job.release_location)]
            vm = dc.add_vm_instance(
                vm_name = job.VM_instance,
                n_nodes = job.n_nodes
            )
            
            footprint = dc.get_trace_footprints(
                timestamp=job.release_time,
                runtime=job.runtime, 
                vm_instance=vm
            )

            dc.vm_instances.remove(vm)
            del vm

            footprints[(job.release_platform, job.release_location)].append(footprint)

        return footprints
