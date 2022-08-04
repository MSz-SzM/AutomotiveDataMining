Imagine a situation where you have two different systems that detect objects. Let us assume that we are using two different neural networks. How to compare the quality of their detection? Can you tell which one is better?

An example in this directory helps you find the answers to the above questions. We show how to combine the outputs of two systems. In the automotive industry, as a rule, we are dealing with the comparison of the AI system's output with the groundtruth data.

Our method enables:
1. Comparison of AI output with GT data.
2. Compare the outputs of two different releases of ML models.
3. Comparison of ReSim (open loop SiL) operation with replay-HiL or a vehicle..
4. .... and many more.

The described method works not only in the automotive industry. You can use it to analyze the outputs of any ML models where the output is a set of bounding boxes.
