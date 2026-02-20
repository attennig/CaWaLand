
# Reproducibility Repository for: **"Spatio-Temporal Shifting to Reduce Carbon, Water, and Land-Use Footprints of Cloud Workloads"**  

*Authors: [Giulio Attenni](https://attennig.github.io), [Youssef Moawad](https://devdude.me), [Novella Bartolini](https://sites.google.com/view/novellabartolini/home), [Lauritz Thamsen](https://lauritzthamsen.org)*



This repository contains the code, data, and documentation required to reproduce the experiments and results presented in the paper: "Spatio-Temporal Shifting to Reduce Carbon, Water, and Land-Use Footprints of Cloud Workloads". Currently under review, [read here](https://arxiv.org/abs/2512.08725)
The repository aims to make our analysis transparent and fully reproducible.


## 🗂️ Repository Structure

```
├── README.md                       # This file
├── data/                           #
│   ├── energy_mix/historical.zip   # historical energy mix data archive
│   ├── providers/                  # regions / data centers data 
│   └── traces/                     # spark and faas traces 
├── experiments/
│   ├── in/                         # This folder is for preprocessed input
│   ├── out/                        # 
│   |   ├── /aws/summary.csv        # AWS result summary
│   |   └── /azure/summary.csv      # Azure result summary
│   └── scenarios/                  # YAML files to change scenario settings
├── notebooks/                      # Reproducibility
├── preprocessing/                  # Helper functions to preprocess data
├── postprocessing/                 # Helper functions to summarize results
├── scripts/                        # Bash scripts to preprocess data
├── src/
│   ├── models/                     # Simulated entities and algorithms
│   ├── parameters.py               # Coefficients and time
│   └── run.py                      # Main experiment runner
└── LICENSE
````


## 📊 Data

The dataset used in this study is available at:

🔗 [Spark Traces](https://github.com/oxhead/scout)

🔗 [Azure Traces](https://github.com/Azure/AzurePublicDataset/blob/master/AzureFunctionsDataset2019.md)

🔗 [Energy Mix - Sweden ](https://transparency.entsoe.eu)

🔗 [Energy Mix - United Kindom ](https://carbon-intensity.github.io/api-definitions/#get-generation-from-to)

🔗 [Energy Mix - Germany ](https://www.smard.de/en/downloadcenter/download-market-data/)

🔗 [Energy Mix - Ercot ](https://www.eia.gov/electricity/wholesalemarkets/data.php?rto=ercot)

🔗 [Energy Mix - Miso ](https://www.eia.gov/electricity/wholesalemarkets/data.php?rto=miso)

🔗 [Energy Mix - Pjm ](https://www.eia.gov/electricity/wholesalemarkets/data.php?rto=pjm)

🔗 [Energy Mix - Caiso ](https://www.eia.gov/electricity/wholesalemarkets/data.php?rto=caiso)


---

## 🧪 Reproducing the Experiments

Execute the "Ecpleriments Reproducibility.ipynb" Jupyter notebook in the `notebooks/` folder. 

---

## 🧩 Version Information

* Python: 3.13.0
* Libraries: requirements.txt

---

## 📜 License

This repository is licensed under the [Hippocratic License 3.0](https://firstdonoharm.dev/build/)

---

<!--  ## 📚 Citation

If you use this code or dataset, please cite:

```
@article{doe2025title,
  title={Title of the Journal Article},
  author={Doe, Jane and Smith, John},
  journal={Journal of Example Research},
  year={2025},
  doi={10.xxxx/xxxxx}
}
```

---
-->


## 🤝 Contact

For questions, please contact:

**Giulio Attenni**
📧 attenni[at]di.uniroma1.it

---