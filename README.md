## OpenSetPerf
A Practitioner's Guide to the Performance of Deep-Learning Based Open Set Recognition Algorithms for Network Intrusion Detection Systems

### Steps to run:

- Clone the repository using the following commands:

`git clone https://github.com/bayegaspard/OpenSetPerf.git`
- Make sure you do that from the `dev` branch.
- Download the [Payload-Byte NIDS Dataset](https://github.com/Yasir-ali-farrukh/Payload-Byte/tree/main/Data) 
- Navigate to the root folder and place the downloaded CSV file in the `dataset` folder. New structure will be `dataset\Payload_data_CICIDS2017.csv` for the CIC dataset and `dataset\UNSW-NB15`.
- If you don't have pip3 installed, you can use the command below to install one.

# varMax
Towards Confidence-Based Zero-Day Attack Recognition.

Official repository for the paper implementation of varMax published at the IEEE Military Communications Conference (IEEE MILCOM) held on 28 October – 1 November 2024 // Washington, DC, USA C5I Technologies for Military and Intelligence Operations Today and Tomorrow, under Track 5 - Machine Learning for Communications and Networking.
### Abstract
Open Set Recognition (OSR) is the ability of a machine learning (ML) algorithm to classify the known and recognize the unknown. In other words, OSR enables novelty detection in classification algorithms. This broader approach is critical to detect new types of attacks, including zero-days, thereby improving the effectiveness and efficiency of various ML-enabled mission-critical systems, such as cyber-physical, facial recognition, spam filtering, and cyber defense systems such as intrusion detection systems (IDS). In ML algorithms, like deep learning (DL) classifiers, hyperparameters control the learning process; their values affect other model parameters, such as weights and biases, which affect the performance of OSR algorithms. Moreover, OSR introduces additional parameters, making DL classifiers bigger and training them more computationally intensive. Determining the suitable set of hyperparameters and parameters is a computationally expensive task. Alternative OSR algorithms have demonstrated promising results on image datasets, but only limited studies have been performed in the context of IDS. This paper proposes OpenSetPerf, an empirical investigation of three prominent OSR algorithms using a current, real-world network intrusion detection systems (NIDS) benchmark dataset to discover the relationship between the DL-based OSR algorithm's hyperparameter values and their performance. OpenSetperf evaluates these algorithms using quantitative studies with widely used ML performance evaluation metrics.

### Installation
```
$ git clone https://github.com/bayegaspard/OpenSetPerf.git
$ cd OpenSetPerf
$ pip install -r requirements.txt
```
### Datasets
Refer to : [Payload-Byte](https://github.com/Yasir-ali-farrukh/Payload-Byte.git)


### Architecture of varMax

<img 
 style="text-align: center;"
 src="https://github.com/user-attachments/assets/95ed090b-3e0a-407e-9f2c-a37f065a802c">

</img>


Cite
```
@inproceedings{baye2024varmax,
  title={varMax: Towards Confidence-Based Zero-Day Attack Recognition},
  author={Baye, Gaspard and Silva, Priscila and Broggi, Alexandre and Bastian, Nathaniel D and Fiondella, Lance and Kul, Gokhan},
  booktitle={MILCOM 2024-2024 IEEE Military Communications Conference (MILCOM)},
  pages={863--868},
  year={2024},
  organization={IEEE}
}
```
### Acknowledgement
> This work has been funded by UMass Dartmouth and was supported by the U.S. Military Academy (USMA) under Cooperative Agreement No. W911NF-22- 2-0160. The views and conclusions expressed in this paper are those of the authors and do not reflect the official policy or position of the U.S. Military Academy, U.S. Army, U.S. Department of Homeland Security, or U.S. Government. Usual disclaimers apply.
