## OpenSetPerf
A Practitioner's Guide to the Performance of Deep-Learning Based Open Set Recognition Algorithms for Network Intrusion Detection Systems

Official repository for the paper implementation of OpenSetPerf published at the IEEE NOMS 2023-2023 IEEE/IFIP Network Operations and Management Symposium.

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


Cite
```
@inproceedings{baye2023performance,
  title={Performance analysis of deep-learning based open set recognition algorithms for network intrusion detection systems},
  author={Baye, Gaspard and Silva, Priscila and Broggi, Alexandre and Fiondella, Lance and Bastian, Nathaniel D and Kul, Gokhan},
  booktitle={NOMS 2023-2023 IEEE/IFIP Network Operations and Management Symposium},
  pages={1--6},
  year={2023},
  organization={IEEE}
}
```
### Acknowledgement
> This work has been funded by UMass Dartmouth and was supported by the U.S. Military Academy (USMA) under Cooperative Agreement No. W911NF-22- 2-0160. The views and conclusions expressed in this paper are those of the authors and do not reflect the official policy or position of the U.S. Military Academy, U.S. Army, U.S. Department of Homeland Security, or U.S. Government. Usual disclaimers apply.
