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

Note:
the sinusoidal function is used for visualization purposes only. It plots the original sinusoidal function, along with the fitted polynomial curve to compare how well the polynomial regression model approximates the sinusoidal function.

While the model itself is trained using polynomial features and SGD for polynomial regression, it's helpful to visualize the original sinusoidal function alongside the fitted polynomial curve to understand how well the model captures the underlying pattern in the data. This comparison allows for an intuitive assessment of the model's performance in approximating the original function.
SGD with validation set
Stochastic Gradient Descent (SGD) with Validation Set for Linear Regression it uses stochastic gradient descent for training a linear regression model and includes a validation set for monitoring model performance during training.
Final parameters: [ 0.87718563 -1.35291406 -0.87747087 -1.58392561  1.76078649  0.74242553]
Final Loss on Training Data: 0.09644533618152092
Final Loss on Testing Data: 0.1418505636242852
Summary from the output
The two plots illustrate the performance and convergence of the Stochastic Gradient Descent (SGD) algorithm for polynomial regression up to degree 5. The first plot, showing training and validation loss versus epochs, indicates a successful learning process where both losses decrease steadily over time, suggesting the model is fitting the data well. The final training loss is approximately 0.0964, and the validation loss is around 0.1419, indicating a reasonable fit with minor overfitting.

The second plot visualizes the fitted polynomial curve against the training data and the original sinusoidal function. The fitted polynomial curve not too closely follows the true sinusoidal pattern, but it could capture some the underlying trend despite the noise in the training data. Although polynomial regression can capture non-linear patterns, it might not perfectly mimic a smooth sinusoidal curve, because our synthetic data is noisy.( includes normally distributed noise with a standard deviation of 0.25.)

The final model parameters reflect the coefficients of the polynomial terms, demonstrating the model's ability to generalize the sinusoidal relationship within the given data range.


Problem 4: SGD Enhancements (30 points)
In this exercise you will implement some enhancements to the implementation of Problem 3 (the linear regression problem) that can improve the convergence speed of the algorithm. Implement from scratch the following enhancements and compare the convergence speed of each algorithm to the baseline SGD algorithm

Momentum (15 points) Adam (15 points) Clearly state the hyperparameters you used and present the loss vs epoch plot that demonstrates the convergence of each algorithm and compared to the baseline SGD algorithm. You can include all plots in the same figure.
Comparison of Optimization Algorithm Convergence: SGD vs. Momentum vs. Adam---Train Loss
Final Test Loss Values:
SGD: 0.17713690172309549
Momentum: 0.17687183271298335
Adam: 0.12093600144525002

Interpretation from Loss Curves: Adam, Momemtum, Sgd
The loss curves for the SGD, Momentum, and Adam optimizers reveal distinct performance differences in polynomial regression tasks. Adam outperforms both SGD and Momentum, as evidenced by its rapid decline in both training and test loss, stabilizing at a significantly lower final test loss of 0.1209. This superior performance is due to Adam's adaptive learning rate mechanism and bias correction terms, which enable faster and more stable convergence. Momentum also shows improvement over vanilla SGD by incorporating a momentum term, resulting in a more rapid and consistent decline in loss, with a final test loss of 0.1769. In contrast, SGD has the slowest convergence and the highest final test loss of 0.1771, reflecting its susceptibility to noise in gradient estimates and simpler update rule.

Analyzing the test loss plot, we notice noise in all three curves, indicating fluctuations in the model's performance on unseen data during training. However, Adam consistently maintains the lowest test loss throughout, suggesting better generalization compared to SGD and Momentum. While Momentum exhibits slightly better performance than SGD.
