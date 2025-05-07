__________NOTES____________________________

EXPERIMENTS
arrival time -> with different distributions
pick interesting datacenter


Scenarios:
single provider experiments

- nextflow -> gcp
- scout -> aws
- AI ->
 -- alibaba 
 -- nvidia, where? on a cloud?

Algorithms:
metaheuristics + greedy + optimal
baseline + SoA


OBSERVATIONS:
- we chose batch processing jobs. During migration we consider only the input size and we assume that migratig the code has negligible cost


___________TODO____________________________
 - Nextflow traces
 - comparison migration vs. no migration


___________TOFIX____________________________

____________________________________________
issues:
Thr 17
- how to compute expected runtime? -> pick executions from the trace, not optimize the scaleouts. mimic runtime adding error. search in the lit. 
 -- e.g. for predicting the runtimes of Spark dataflows we can derive some realistic errors from https://arxiv.org/abs/2107.13921 and https://arxiv.org/abs/2107.13317
Bellamy: Reusing Performance Models for Distributed Dataflow Jobs...
Distributed dataflow systems enable the use of clusters for scalable data analytics. However, selecting appropriate cluster resources for a processing job is often not straightforward. Performance...
---- Bellamy seems to be perfect for what I need, but I cannot install environment properly

==> scout spark traces have runtime <= 1h -> there won't be any migration
 - geographical approach -> each job is executed where it is submitted and with the requested configuration (from historical data)
 - objective w VM capacity constraint -> each job is executed in the best DC that has the requested configuration available
   -- What if there are not enough VM of a certain type across all DCs? job get delayed or we avoid such scenario


____________________________________________

1) we have a job that comes with a configuration --> historical runtime with noise --> the decision is in which datacenter we want use such configuration

We also want to plan when

one region with different availabilities -> same energy mix
multiple regions 



_____________________________________________
to schedule:
- how to account for migration costs -> carbon aware networking, check out 
    --> amount of data - resource util
    --> bandwithd 

 -v-Seminar #21 2023-03-16: Noa Zilberman 
 -v-Seminar #29 2023-11-30: Jonghoon Kwon "Carbon-Aware Global Routing in Path-Aware Networks"

_____________________________________________



___________DONE___________________________

Wed 23, Fri 25
==> theory, our problem is not NP-hard and can be solved reducing it to the unbalanced assignment probleb.

Tue 22, Wed 23
- location arrival distribution
 -- https://www.ml.cmu.edu/research/dap-papers/dacheng_dap_final.pdf generative process, Hierarchical Bundling Mode able to mimic multiple components in the distribution of IAT, and to simulate job requests with the same statistical properties as in the real data  https://doi.org/10.1007/978-3-319-06605-9_17
==> 
 -> mimic the original distribution of spark traces considering DC timezone
  - consider scout spark traces
  - extract arrival distribution considering for each hour the avarege number of jobs (over available dates)
  - regression model, 5th degree polynom
  - for each datacenter 
     - generate a random distribution for job arrival (useing mae to estimate std_dev and add noise to the model fit)
     - shift the distribution according to the datacenter timezone
     - according to the shifted distribution for each hour pick uniformally at random traces from the original dataset and change the arrival_time to such hour of the simulation horizon
    
Wed 16
- use forecast data, not historical -> *mimic forecast with reported error*,  try to find data with both forecast + historical. Marginal california watttime
==> 
 ->  simulate forecast data by "noising" the real values in a way that mimics real electricity maps forecasting errors.
  - Add noise to renewable sources (randomly disturb the individual renewables).
  - Compute the delta between actual total renewables and noisy renewables.
  - Adjust non-renewables proportionally to their actual share to keep total production fixed.

- IPCC coefficients    
- normalize intensity coefficients



-----------
find a paper that predicts source mix 