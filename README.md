# cs670-Assignments
Problem 1A (15 points)
Simulate (sample from) the bivariate normal distribution with the shown parameters obtaining a plot similar to Figure 6.8b that shows the simulation result from a different bivariate Gaussian distribution. You can generate m=200 samples/points

parameters: Mean vector: μ = [0, 2] Covariance matrix: Σ = [[0.3, -1], [-1, 5]]

Plot Interpretation
Scatter Plot: The blue dots represent the 200 samples generated from the bivariate normal distribution. These points are scattered across the plot, with their distribution determined by the mean vector and covariance matrix specified in the question.

Mean Point: The red cross represents the mean of the bivariate normal distribution, which is set at coordinates (0, 2) according to the provided mean vector because it represents the average values of the two variables being considered.

Contour Lines: The contour lines represent regions of equal probability density in the bivariate normal distribution. Areas with higher density are represented by closely spaced contour lines, while areas with lower density have more widely spaced contour lines. The contour lines bend and stretch to capture the shape of the distribution based on the covariance matrix. If there are points in the plot that are not covered by contour lines, it suggests that these regions have lower probability density.

Problem 1B (5 points)
Plot the contours of the bivariate Gaussian distribution and the simulated points in the same plot. (5 points)
Problem 2: Projection (20 points)
Simulate a 3-dimensional (3d) Gaussian random vector with the following covariance matrix by sampling m = 1000 3D vectors from this distribution.

[4, 2, 1 2, 3, 1.5 1, 1.5, 2]

Using the Singular Value Decomposition (SVD) of the covariance matrix compute the projection of the m simulated vectors onto the subspace spanned by the first two principal components (or left singular vectors of the covariance matrix).

Problem 2A (5 points)What determines the principal components ? Show the vectors which denote the first 2 principal components.
The principal components are determined by performing Singular Value Decomposition (SVD) on the covariance matrix of the data. The left singular vectors (or eigenvectors) of the covariance matrix represent the principal components. The first principal component corresponds to the eigenvector with the largest eigenvalue, and the second principal component corresponds to the eigenvector with the second-largest eigenvalue.

For the given data, the vectors denoting the first two principal components are:

First principal component: ([-0.70173922, -0.60421021, -0.37748125])
Second principal component: ([0.68097512, -0.41315066, -0.60463164])
These vectors represent the directions of maximum variance in the data, with the first principal component capturing the most variance and the second principal component capturing the second most.
Problem 2B (5 points)
Plot the projected vectors in the subspace of first 2 principal components.

Projecting the simulated vectors onto the subspace spanned by these first two principal components. Plotting these projected vectors in a 2D space, where the x-axis represents the first principal component and the y-axis represents the second principal component.
Problem 2C (10 points): Reverse the projection to map back to the original 3D space and create a scatter plot to show the reconstructed points. Do the reconstructed points have identical/similar but not identical/different correlations in respective components as the original matrix?
I have multiplied the projected vectors (which were projected onto the subspace of the first two principal components) by the transpose of the first two principal components. This will map the vectors back to the original 3D space.

Then plotted the reconstructed points in a 3D scatter plot. Each point represents a reconstructed vector in the original 3D space.

Compare Correlations: Analyze whether the correlations between the components of the reconstructed vectors are identical, similar but not identical, or different from those in the original matrix. This involves comparing the covariance structure of the original data with that of the reconstructed data. If they are similar, it suggests that the projection and reverse projection preserved the structure of the data.

Interpretation of the Plot
X-axis: Represents one of the components in the original 3D space. Y-axis: Represents another component in the original 3D space. Z-axis: Represents the third component in the original 3D space.

In this plot, each point represents a reconstructed vector in the original 3D space

I notice that the reconstructed points closely resemble the original data points, it indicates that the projection and reverse projection processes were successful in preserving the structure of the data.

Do the reconstructed points have identical/similar but not identical/different correlations in respective components as the original matrix?
The reconstructed covariance matrix is quite close to the original covariance matrix, suggesting that the overall variance and covariances between variables were preserved reasonably well during the projection and reverse projection processes.

The correlation matrix of the reconstructed data shows some differences compared to the original correlation matrix. While the diagonal elements (which represent the correlation of each variable with itself) remain 1, the off-diagonal elements (which represent the correlations between different variables) show some variations. Overall, the correlations in the reconstructed data appear to be similar but not identical to those in the original data.

Problem 3: Stochastic Gradient Descent (30 points)
In class we covered the baseline stochastic gradient descent. Using the linear regression example from the class notes, develop from scratch the baseline SGD algorithm. :

Clearly state the hyper-parameters you used and present the loss vs epoch plot that demonstrates the convergence of the algorithm.
Final Training Loss: 0.15482186564672237
Final Validation Loss: 0.1471253637667969

Summary from the output
Throughout training, both the training and validation losses decrease gradually, indicating that the model is effectively learning the underlying patterns in the data. However, there is a noticeable distinction between the two curves: while the training loss decreases consistently, the validation loss shows a slightly longer tail, indicating that the model's performance on unseen data is not as optimized as its performance on the training set.

Nonetheless, the final training and validation losses, 0.155 and 0.147 respectively, are relatively close, suggesting that the model's generalization performance is reasonable. The final learned parameters, approximately [0.329, -0.922], represent the coefficients of the linear regression model, indicating the intercept and slope of the fitted line.

Problem 4: SGD Enhancements (30 points)
In this exercise you will implement some enhancements to the implementation of Problem 3 (the linear regression problem) that can improve the convergence speed of the algorithm. Implement from scratch the following enhancements and compare the convergence speed of each algorithm to the baseline SGD algorithm

Momentum (15 points) Adam (15 points) Clearly state the hyperparameters you used and present the loss vs epoch plot that demonstrates the convergence of each algorithm and compared to the baseline SGD algorithm. You can include all plots in the same figure.

Comparison of Optimization Algorithm Convergence: SGD vs. Momentum vs. Adam---Train Loss
Final Loss for SGD: 0.17871526846096164
Final Loss for Adam: 0.17387841888950195
Final Loss for Momentum: 0.17815035757644676

Interpretation from Loss Curves: Adam, Momemtum, Sgd
The final losses for the three optimizers are as follows: SGD - 0.1787, Adam - 0.1739, and Momentum - 0.1782. Adam achieved the lowest final loss among the three, indicating its superior performance in minimizing the loss function. Momentum and SGD had slightly higher final losses, with Momentum being marginally better than SGD.

Examining the training loss plot, we observe that initially, all three optimizers show a rapid decrease in loss, indicating effective learning. However, as training progresses, the curves start to plateau, with Adam maintaining a consistently lower loss compared to the other two. Interestingly, the SGD and Momentum curves indeed align closely, suggesting that Momentum, by considering past gradients during parameter updates, helps SGD (Stochastic Gradient Descent) behave more like advanced optimizers such as Adam. This alignment between the SGD and Momentum curves suggests that Momentum brings some of the benefits of more sophisticated optimization techniques to basic SGD.

Analyzing the test loss plot, we notice noise in all three curves, indicating fluctuations in the model's performance on unseen data during training. However, Adam consistently maintains the lowest test loss throughout, suggesting better generalization compared to SGD and Momentum. While Momentum exhibits slightly better performance than SGD.
