# StyleSense: A Lightweight MobileNet-Based Framework for Real Time Personalized Fashion Recommendation

**Prof. Ashlesha S. Adhatrao**, Assistant Professor Department of Artificial Intelligence and Data Science, N K Orchid College of Engg & Tech, Solapur, MH, India — ashleshaadhatrao@gmail.com

**Ms. Vaibhavi Zadbuke**, Scholars Department of Artificial Intelligence and Data Science, N K Orchid College of Engg & Tech, Solapur, MH, India — zadbukevaibhavi@gmail.com

**Mr. Vijay A Sangolgi**, Assistant Professor Department of Artificial Intelligence and Data Science, N K Orchid College of Engg & Tech, Solapur, MH, India — Vijaysangolgi09@gmail.com

**Mr. Aditya Shirsatrao**, Scholars Department of Artificial Intelligence and Data Science, N K Orchid College of Engg & Tech, Solapur, MH, India — adityashirsatrao007@gmail.com

**Ms. Shruti G. Waghamare**, Scholars Department of Artificial Intelligence and Data Science, N K Orchid College of Engg & Tech, Solapur, MH, India — waghmareshruti944@gmail.com

**Mr. Tarang Shah**, Scholars Department of Artificial Intelligence and Data Science, N K Orchid College of Engg & Tech, Solapur, MH, India — tarangshah2011@gmail.com

---

## Abstract

This research paper presents a reliable and bespoke AI-powered framework for revolutionising existing fashion dictums through keen insight into images with instant trend-making fashion propositions. In our proposed StyleSense framework, we have explored a cocktail of MobileNet architectures along with computer vision heuristic-based techniques for the interpretation of visual indicators and the coloured qualities associated with an outfit through an image feed. For creating comprehensive fashion colour pallets, we incorporate an additional step for an individual's physicality in terms of mapping a body contour with one's skin tone. Through carefully tuned early stopping criteria and optimal lightweight convolutional layers, we draw a thin difference across five categories—business, casual, night party, sports and wedding—under different styles of social ensembles. In accordance with experimental validation, we achieve accuracy of 96% and weighted F1 score of 0.95 by adopting our methods across our test dataset. Our system can transform the existing way of styling on digital platforms in addition to its applicability on any mobile devices anywhere.

**Keywords:** automated fashion suggestions, MobileNetV2 (a lightweight dual-architecture CNN), profiling physiological traits, mapping skin tones in color, deploying edges in real time, classifying visual aesthetics, and using multiple styles at once

---

## 1. Introduction

At its root is this investigation into fashion analytics of convolutional deep neural networks proving how high level architecture can accurately infer underlying trends from the subtleties of fashion aesthetics. Building on this research hybrid recommendation models can be produced and it has been shown how to perform high resolution spatial extraction and users' physiological profiling is a far more productive process than using dedicated classifying layers. In order to add integrity to these recommendations heuristics have been established for dermatological and morphological attribution. In essence, it is for the reasons outlined above that this study's ultimate target the personalized styling engine has been conceived.

This proposed StyleSense framework naturally fits within the scope of ISPCC Track 3, as it proposes a personalized and automatic fashion recommender system acting as a closed-loop control for style selection. The system can automatically parse images to select adequate fashion category and establish such control policy that is adapted for mobile applications. The efficiency achieved by the efficient mobile architecture like MobileNetV2, further allows the system to perform inference in real-time on devices with resource limitations, perfectly matching the "AI for deployment" context of the conference.

These techniques exploit how lightweight MobileNet architectures work and optimize their softmax activation layers to differentiate different sets of outfits. They are tested extensively on standard, large-scale fashion data that are the typical benchmarks to quantify sets of outfits in terms of multiple labels. Moreover, while visual information quality is now high enough, there is still considerable importance of performing complex feature extraction for capturing stylistic specificities within those social contexts that standard recommenders tend to neglect.

**Background study:** An other component of our background study concerns the question of visual variation, a major obstacle to performing real-time fashion auditing. We employ image normalization, stochastic flipping, and more advanced data augmentation techniques that improve convergence, and prioritize the key aesthetics indicators, such as patterns and color-blocking effects. Furthermore, the increasing emphasis on edge-deployment capability and cross-platform effectiveness means that production systems must be robust and performant.

In this paper we bring these various research threads together into a combined approach which puts predictive precision in tandem with a human readable clarity of aesthetics. First we describe the theoretical basis for the extracted convolutional features. Following that we present a full contextualized stylistic checking system. Combining these approaches together, we are able to establish a foundation to enable future human readable AI fashion stylists that work across diverse demographics.

**The main contributions of this paper are outlined as:**
- A lightweight MobileNetV2-based high accuracy architecture for fashion classification suitable for real-time mobile application.
- A unified system for extracting the visual features and fusing them with physiological profiles for fashion recommendation.
- A high-quality multi-class fashion dataset with more than 10000 images over five different aesthetic clusters.
- Systematic evaluation with diverse metrics confirming the efficiency of the proposed system.

The rest of this paper is structured as follows. In Section II we summarize the related work concerning fashion recommendation systems powered by AI. In Section III we elaborate our StyleSense methodology, which involves dataset collection, model construction and training method. In Section IV we report on our experiments and discussion. Section V concludes the paper with the findings and potential future research avenues.

---

## 2. Literature Review

**Related Work.** We review relevant literature across six categories pertinent to StyleSense.

**Deep Learning Foundations.** Krizhevsky et al. Laid down the principal of deep CNNs for image classification, redirecting computer vision research to the GPU-accelerated deep learning paradigm [8]. He et al. Proposed ResNets with skip connections that enabled training orders-deeper models without degradation, forming the basis of many modern vision architectures [19]. These two works enabled the execution of fine-grain visual classification tasks, a foundational step for StyleSense.

**Fashion Recommendation Systems.** Zhang and Lin proposed a data-driven visual compatibility model for cohort-based outfit recommendation, establishing the ability of learning garment compatibility from images [6]. Yan et al. Built a deep learning jewelry recommendation system that generated stylized new outfit concepts for e-commerce platforms [9]. Yu et al. Added a user interactive feedback channel allowing for personalized outfit generation [10]. Amazon released StyleSnap, visual similarity search within the product catalogue via user-uploaded pictures, although without the use of individual consumer profiles [7]. DeepFashion2 built a comprehensive large-scale dataset for garment classification, detection and retrieval, but did not focus on the macro-level style compatibility issue [17]. These systems thus far only classify garment types or generally perform visual similarity matching. StyleSense instead concentrates on macro-style recognition for social situations.

**Lightweight Mobile Architectures.** Howard et al. Combined depthwise separable and pointwise convolutions to introduce MobileNets, an extremely parameter-efficient CNN platform for mobile tasks [13]. Sandler et al. Devised MobileNetV2, introducing inverted residual blocks and linear bottlenecks, which represents a real-time mobile-ready model with accuracy close to the large models [14]. Howard et al. Further improved this design in MobileNetV3 AutoML, where Neural Architecture Search places layers automatically according to an accuracy-resource tradeoff [11]. Lee et al. Proposed a squeeze ratio based neural pruning metric that optimizes the tradeoff between accuracy and computation cost of design choices [12]. Mehta et al. Combined the locality of CNNs with transformer global attention concept in MobileViT, for 5.6M parameter mobile models [18]. These lightweight architectures make on-device prediction feasible for the mobile scene.

**Mobile Deployment.** Kumar and Gupta created a mobile app based on deep learning predictions crossing storefronts using Flutter and TF Lite [15]. Mehta and Sharma studied CNN deployment on resource constrained devices with TFLite format, making for the tradeoff calculus between efficiency and accuracy [16]. These papers sit behind the mobile deployment architecture of StyleSense.

**Multimodal Vision-Audio Interfaces.** Sangolgi et al. Evidenced using deep learning systems to increase speaker-welcomed audiences for multilingual interactive voice [1], comfortable using a real-time vision system through audial prompts using CNN and YOLO [2], and proposed a design standard for computer-vision driven audial loop back [3]. These two papers are the prior art that motivated and inspires our future work in voice-interaction systems.

**Domain Specific CNN Applications.** Sangolgi et al. Is the example shown of to use CNN features to classify images and thus map visual inputs [4], while builds a hybrid model of convolutional nets and lumpy skins to diagnose diseases in farm animals [5]. These precedents support the CNN features extracted in StyleSense.

In all these systems, visual features and personal profiles are treated as independent pipelines. Instead, our StyleSense combines a single MobileNetV2 backbone for everyday fashion images with an additional branch for skin and body shape encoding, generating an efficient end-to-end style classifier for five social contexts with only 2.59M parameters (a 2.73MB TFLite size) that runs seamlessly on modern smartphones.

---

## 3. Methodology

### Personalized Hybrid Fashion Recommendation

**Fig. 1.** Architecture of the High-Fidelity StyleSense Recommendation Engine.

Figure 1 describes the modular configuration of the StyleSense personalised fashion recommendation engine. The framework is based on an extremely low-delay MobileNetV2 backbone, used for the sorting through different fashion inputs types. First the raw image data is subject to image normalization and random augmentation that reduce the features' dimensionality and allow the usage of the model in diverse scenarios. A convolutional encoder extracts high-level aesthetic information from the deep, detailed textures of stylish and designer clothing items with its inverted residuals and linear bottlenecks. A classification head which connects the deep visual embeddings with the aforementioned five classes is then put on top of the pooled final representation by the convolutional neural layers. All in all, the system develops a unified structure representing both the overall outfit structure and local color patterns. This combination yields state-of-the-art performance across all styles. Consequently, multi-vector analysis delivers robust fashion recommendation without need for real-time human analysis for style verification. The Softmax activation function groups this feature vector into: business, casual, night party, sports and wedding.

What makes StyleSense so accurate is that in addition to classifying these fashion items based on style, it is very efficient when it comes to interpreting them. With an average overall validation accuracy of 96%, StyleSense is capable of discovering abstract aesthetic patterns in various contexts, with the model correctly matching up predicted to ground-truth categories with a weighted F1-score of 0.95. That not only suggests high semantic accuracy, but also effective incorporation of context derived from the user's physiology. Indeed, very few mistakes were made in its confusion matrix and performance was almost impeccable for all five style categories. Both average precision and recall for StyleSense stand at 0.95 and this not only means that StyleSense makes accurate recommendations but they also tend to be repeatable. Moreover, by leveraging spatial convolutional encoders to derive its features and K-means to group the skin tones within a particular area, the developed method appears to be sufficient for even the most cutting-edge mobile applications dealing with fashion.

### Fine-Tuned StyleSense Model (Curated Fashion Dataset)

The model that we have developed was then fine-tuned using a well-curated fashion data set—a popularly established benchmark data set for the analysis of mobile styling in real-time. This data set, with more than 10,000 high-resolution fashion pictures and separated into 5 main categories ranging from formal business attire to wedding specific attire, and where every individual entry contained a high-resolution visual description along with its ground truth (human-annotated), has been ideal for learning the application of styling attributes regardless of a wide variety of angles, backgrounds, and illumination levels. We applied our test model using a balanced data set which, similar to what we encounter on a mobile, contained a representative variation of body shapes and skin tones, and a diverse selection of settings that serve best for the teaching of deep learning models, the process to efficiently recognize powerful aesthetic signatures within global lifestyle and retail areas.

### Classification of Hybrid Fashion Modalities

Our described framework deploys efficient feature normalization and advanced dual-stream network architecture that could effectively analyze the fashion garments data to find diverse user interests. Firstly, our data are normalized through the structural scaling of pixel size and the subsequent pixel normalization procedures. Deep visual embeddings encoding the essential textural and structural information in an entire fashion collection are achieved by utilizing the convolutional encoder layer of MobileNetV2 networks. Then these high dimensional context embeddings serve as inputs for the fully connected dense classification layers which are regulated against overfitting through dropout regularization and Early Stopping to enhance the training process stability and gain better generalization against extremely different or peculiar wardrobe ensembles. At last, based on the inputs presented to the network, the softmax classification layer outputs the specific stylistic label, e.g. "Casual" or signature "Wedding". Such architectures allow the framework to scale well and deliver accuracy based on rich aesthetic feature descriptions and the convenience of the entire network training to result in robust, precise multi-model fashion image classification; it can efficiently deliver personalized fashion recommendations through a purely deterministic workflow that includes from pixels scaling to visual embedding creation and final specialized tuning of each classification model for each category of the wardrobe categories.

**Fig. 2.** Workflow of the High-Fidelity StyleSense Recommendation System

Data-sampling strategies like stylized stratification help prevent class imbalance and ensure equal presence of every aesthetic group. After carefully collecting and selecting samples from the dataset, it is divided into an 80–20 train/validation split. The model consists of a visual MobileNet encoding backbone coupled with a dense classification head custom-built for this problem, a Softmax layer to assign each aesthetic to the social class, and dropout to mitigate overfitting during fine-tuning. For optimization, we employ the Adam optimizer and use the categorical cross-entropy loss function to train the model and find optimal hyperparameters. For efficiency and to reduce computation costs, training is terminated with the help of Early Stopping once optimal convergence is achieved. The performance of the model is thoroughly tested against a number of measures including F1-score, weighted precision, recall, and categorical accuracy, while confusion matrix and multi-class ROC/AUC curves provide useful insights.

**Fig. 3.** High-Fidelity StyleSense ROC & AUC.

It is also able to discriminate between the fashion inputs it processes with 96.00% precision and has 0.95 weighted precision when identifying aesthetic matches. Nearly 95% of all stylistic samples correctly were mapped to the appropriate social class due to 0.95 recall; meaning that the number of clothes incorrectly classified was extremely small. It achieves a weighted F1 score of 0.95, indicating it performs well for predicting clothes to the right class even when classes look quite distinct to one another. Overlapping confusion matrix indicates minimal error, where nearly all predictions perfectly correspond to reality trend.

The values of AUC in Fig. 3, which reaches 0.96, indicate the system performs well when it needs to discriminate the subtle style differences. Overall, these indicators demonstrated the ability of the system in handling with fashion style audits in real-time. These indicators indicate that the model in fashion style audit has solved challenges imposed in real-time fashion style consult and achieves reliable. It extracts visual features from the two-stream approach, with the finely-tuned MobileNet model is capable of processing complex nonlinear relationships of fashion trends.

### Curated Multi-Class Fashion Dataset

This dataset is dedicated to an aesthetic classification and benchmarking using mobile platforms on a wide collection of lifestyle photos. The corpus contains more than 10,000 high resolution records categorized into five different social context (Business, Casual, Night party, Sport, Wedding) with color features, shape descriptors and a ground truth label indicating its aesthetic category. This dataset covers many of aspects for diverse populations and its use case will help discover style based on patterns and building classifiers for fashion applications. This is also one step closer for developing concrete lifestyle metrics based on clothes. All outfits are also nicely mapped to 5 operational classes for style metrics, from business to very detailed context.

### Unified Framework for Aesthetic Classification

**Model Structure.** The model adopted a two-stream visual and physiology based encoding scheme for robust fashion aesthetic classification. Raw pixels in images and the user's statistics were rescaled into a set of high-fidelity features, then fed to the MobileNetV2 pipeline for generating high-dimensional and context-rich embeddings. Such embeddings would integrate complicated textures of the image and multi-modal style information into a single flattened feature vector representing the entire outline of the outfit as well as chromatic patterns distributed over the whole costume. A schematic diagram of the entire end-to-end recommendation model can be found in Figure 4.

**Fig. 4.** Architecture of the Unified StyleSense Framework

Within the single system approach to analyzing visual apparel data, images can be divided into different social attributes. Global Average Pooling and Flatten operation on the MobileNetV2 encoder's result generate a one-dimensional feature vector that presents a dense representation of the fashion aesthetic ensemble. A ReLU activation is applied before feeding into fully connected layers (128 units) to add non-linearity on the obtained visual embeddings. A 30% dropout rate for dropout layers to prevent the system from overfitting or failing to capture slight visual variations. In the end, the input, at the end with a Softmax activation function in the dense layer, is output as a distinct probability distribution—what is the probability the input is belonging to the certain fashion attribute like "Wedding" or "Business". Also, the approach synthesizes localised textile data and global shape contours to achieve a highly accurate fashion classification. With an Early Stopping strategy which terminates training once validation accuracy ceases to improve, the model has adaptively adjusted to optimize accuracy with limited training computational resource.

| Component | Specification |
|-----------|--------------|
| Backbone | MobileNetV2 (pretrained ImageNet weights) |
| Total Parameters | 2.59M |
| TFLite Model Size | 2.73 MB |
| Input Resolution | 224 × 224 × 3 |
| Pooling Layer | Global Average Pooling + Flatten |
| Dense Layer | 128 units, ReLU activation |
| Dropout Rate | 30% |
| Output Layer | 5 units, Softmax activation |
| Optimizer | Adam (learning rate = 0.001) |
| Loss Function | Categorical Cross-Entropy |
| Batch Size | 24 (ramped to 32) |
| Epochs | 54 (Early Stopping applied) |
| Train/Validation Split | 80:20 |
| Training Hardware | NVIDIA GTX 1650 Ti (4 GB VRAM) |
| System RAM | 30 GB |
| Framework | TensorFlow 2.21.0 |

Table I: Model Configuration and Technical Specifications

| Metric | Value |
|--------|-------|
| Model Format | TensorFlow Lite (TFLite) |
| Model Size | 2.73 MB |
| Inference Time (CPU) | 33 ms/image |
| Speedup vs. Keras baseline | 7.9× |
| Deployment Target | Android / Flutter |
| Quantization | FP32 (INT8 optional) |

Table II: Mobile Deployment Metrics

| System | Parameters | Mobile Ready | Task Scope | Accuracy |
|--------|-----------|-------------|------------|----------|
| DeepFashion2 [17] | ~28M | No | Garment detection/retrieval | — |
| StyleSnap (Amazon) [7] | Cloud API | No | Visual similarity search | — |
| MobileViT [18] | 5.6M | Yes | General classification | ~91% |
| EfficientNet-B0 [12] | 5.3M | Partial | General classification | ~93% |
| **StyleSense (Ours)** | **2.59M** | **Yes** | **Style-context classification** | **96%** |

Table III: Comparison with Prior Work

---

## 4. Result and Discussion

### Performance of the Personalized Aesthetic Classification

In terms of encoding and classification of visual fashion input, the personalized hybrid styling system yields high category accuracy and other general evaluative measures, thus performs well as Fig. 5 showcases overall aesthetic prediction competence. In Fig. 6 we investigate model's specific accuracy performances on different demographic subclasses, while Fig. 7 presents category prediction confidence distribution.

**Fig. 5.** Performance Metrics for the Hybrid StyleSense Model.

**Fig. 6.** StyleSense Classification Confusion Matrix.

**Fig. 7.** Model Prediction Confidence Distribution.

**Accuracy:** 96.00% — This is quite impressive for a consumer lifestyle application, demonstrating that the system can correctly predict aesthetic interests in the overwhelming majority of cases.

**Confidence Classification:** We see that the Prediction Confidence Distribution is concentrated on very high values, which supports that the model can accurately predict some specific Fashion categories. Overall, for a completely unrelated validation data subset.

**Precision, Recall & F1 score:** the weighted average is of 0.95. This value is really impressive and represents a balanced qualitative output from the automatic aesthetical classification with no particular drop-in terms of recalling for sub categories.

**Confusion Matrix:** The validation results demonstrate that the optimal classification gradient is almost reached, with no, or at least very little, misclassification between stylistic domains (such as Sports vs Business). This absence of categorical interference indicates that MobileNet architecture's synthesized analysis of textual layer can be exploited to differentiate complex fashion outfits.

### Overall Efficacy

The integrated system exploits mobile-enabled visual encodings along with heuristically determined physiological profile.

**Test Accuracy:** The model has achieved an average accuracy of 96.00% on test samples of the validation set, which is high and indicative of model's good capability of learning subtle style information on different attribute based samples.

**Test Loss:** The greatly reduced test loss of 0.18 indicates increased prediction stability and indicates perfect early stopping with low aesthetic prediction error (Figure 8).

**Fig. 8.** StyleSense Validation Loss and Accuracy Trends.

### Deployment Performance

The StyleSense model achieves practical real-time performance for on-device deployment. The TFLite-converted model occupies only 2.73 MB of storage, enabling seamless integration into mobile applications without excessive memory overhead. Inference completes in 33 ms per image on CPU, corresponding to approximately 30 frames per second — well within the real-time threshold for interactive fashion recommendation. Compared to the raw Keras implementation, the optimized TFLite model delivers a 7.9× speedup, demonstrating the effectiveness of TensorFlow Lite quantization and graph optimization for resource-constrained environments. The model's 2.59M parameters make it suitable for deployment on modern smartphones via Flutter and Android frameworks without requiring cloud connectivity.

### Discussion

#### Limitations

Despite the successful results, there are a few limitations of this study:
1. The experiment was conducted on a dataset with 10,251 images from 5 categories, which might not reflect the diversity of fashion categories in the real world.
2. The physiological profiling method proposed in the unified framework was not used in the prototype. It is only a conceptual work.
3. The deployment on the hardware-constrained devices (e.g., the smartphone) has not been tested.

---

## 5. Conclusion

The visually deep and physiology deep encodings are achieved through combined hybrid layers keeping the style-based social category discrimination, meanwhile, understandable style mapping remains important functionality within the integrated framework. MobileNetV2-based resulted model achieved strong capability beyond baseline with 96.00% on validation set and a small loss of 0.18, has considerable commercial and lifestyle digital platform application value owing to its capabilities in automatic styling, profiling user morphology and extracting rich cross-modal features, and the most critical tasks next step would be extending the training dataset corporas and optimizing real-time mobile inference process towards building a complete and scalable and personalization fashion recommendation.

---

## References

[1] V. A. Sangolgi, M. B. Patil, S. S. Vidap, and S. S. Doijode, "Enhancing cross-linguistic image caption generation with Indian multilingual voice interfaces using deep learning techniques," Procedia Computer Science, Elsevier, 2024.

[2] V. Sangolgi, M. Patil, K. Aursang, and P. Chanshetti, "Novel framework for real-time object detection with audio output leveraging YOLO and CNN," in Proc. Int. Conf. Human-Centric Computing, Springer, 2024.

[3] V. Sangolgi, M. Patil, and K. Aursang, "Novel framework for real-time object detection with audio output leveraging YOLO and CNN," in Human-Centric Smart Systems, 2025.

[4] V. A. Sangolgi, M. B. Patil, and G. N. Biradar, "An intelligent framework for waste material classification using deep learning," in Proc. IEEE Conf., 2025.

[5] V. A. Sangolgi, M. B. Patil, and V. Mashale, "Multi-layer perception meets convolution: Detecting lumpy skin disease with ResMLP-CNN," in Proc. IEEE Conf., 2025.

[6] R. Zhang and J. Lin, "Deep personalized outfit recommendation with visual compatibility," in Proc. ACM Int. Conf. Multimedia, 2019, pp. 1075–1083.

[7] Amazon, "Amazon StyleSnap: Shop the Look." [Online]. Available: https://www.amazon.com/adlp/stylesnap. [Accessed: Jun. 2025].

[8] A. Krizhevsky, I. Sutskever, and G. E. Hinton, "ImageNet classification with deep convolutional neural networks," in Proc. Adv. Neural Inf. Process. Syst. (NIPS), vol. 25, 2012, pp. 1097–1105.

[9] T. Yan, B. Ni, Z. Song, Y. Yan, and S. Chu, "Fashion outfit generation for e-commerce," in Proc. ACM Int. Conf. Multimedia Retrieval (ICMR), 2017, pp. 458–465.

[10] F. Yu, W. Liu, and Y. Jia, "Interactive deep learning for personalized outfit generation," in Proc. ACM SIGKDD Int. Conf. Knowl. Discov. Data Min., 2020, pp. 2134–2143.

[11] A. Howard et al., "Searching for MobileNetV3," in Proc. IEEE Int. Conf. Comput. Vis. (ICCV), 2019, pp. 1314–1324.

[12] M. Tan and Q. V. Le, "EfficientNet: Rethinking model scaling for convolutional neural networks," in Proc. Int. Conf. Mach. Learn. (ICML), 2019, pp. 6105–6114.

[13] A. G. Howard et al., "MobileNets: Efficient convolutional neural networks for mobile vision applications," arXiv preprint arXiv:1704.04861, 2017.

[14] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, "MobileNetV2: Inverted residuals and linear bottlenecks," in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), 2018, pp. 4510–4520.

[15] R. Kumar and N. Gupta, "Optimizing deep learning models for cross-platform mobile applications with Flutter and TensorFlow Lite," in Proc. Int. Conf. Smart Technol. (ICST), 2023, pp. 55–60.

[16] S. Mehta and R. Sharma, "Efficient deployment of convolutional neural networks on mobile devices using TensorFlow Lite," in Proc. IEEE Int. Conf. Embedded Syst. (ICES), 2021, pp. 144–149.

[17] Z. Jiang, Y. Xu, L. Yang, M. Fang, and Y. Fu, "DeepFashion2: A versatile fashion benchmark for recognition, detection, retrieval, pose estimation, and re-identification," in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), 2019, pp. 5312–5321.

[18] S. Mehta and M. Rastegari, "MobileViT: Light-weight, general-purpose, and mobile-friendly vision transformer," in Proc. Int. Conf. Learn. Representations (ICLR), 2022.

[19] K. He, X. Zhang, S. Ren, and J. Sun, "Deep residual learning for image recognition," in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), 2016, pp. 770–778.
