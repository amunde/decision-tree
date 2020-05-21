Decision Tree

This file should learn a decision tree with a specified maximum depth, print the decision tree in a specified format, predict the labels of the training and testing examples, and calculate training and testing errors.

The tree uses Gini index as the splitting criteria.

Execution - 
Type on command line - python decisionTree.py [args...]

Where above [args...] is a placeholder for six command-line arguments: <train input> <test input> <max depth> <train out> <test out> <metrics out>.Theseargumentsarede- scribed in detail below:
1. <train input>: path to the training input .tsv file
2. <test input>: path to the test input .tsv file
3. <max depth>: maximum depth to which the tree will be built
4. <train out>: path of output .labels file to which the predictions on the training data will be written 
5. <test out>: path of output .labels file to which the predictions on the test data will be written
6. <metrics out>: path of the output .txt file to which metrics such as train and test error will be written

eg - python decisionTree.py train.tsv test.tsv 2 train.labels test.labels metrics.txt

Output - 

[15 D /13 R]
| feature_1 = y: [13 D /1 R] | 
  | feature_2 = y: [13 D /0 R]
  | feature_2 = n: [0 D /1 R]
| feature_1 = n: [2 D /12 R] | 
  | feature_2 = y: [2 D /7 R]
  | feature_2 = n: [0 D /5 R]

