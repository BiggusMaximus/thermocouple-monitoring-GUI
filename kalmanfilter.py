import numpy as np
from scipy.linalg import inv

class KalmanFilter:
    def __init__(self, initial_state, initial_covariance, process_noise, measurement_noise, measurement_matrix, control_matrix=None):
        self.state = initial_state
        self.covariance = initial_covariance
        self.process_noise = process_noise
        self.measurement_noise = measurement_noise
        self.measurement_matrix = measurement_matrix
        self.control_matrix = control_matrix

    def predict(self, control_input=None):
        if self.control_matrix is not None and control_input is not None:
            self.state = np.dot(self.control_matrix, control_input) + np.dot(self.measurement_matrix, self.state)
        else:
            self.state = np.dot(self.measurement_matrix, self.state)

        self.covariance = np.dot(np.dot(self.measurement_matrix, self.covariance), self.measurement_matrix.T) + self.process_noise

        return self.state

    def update(self, measurement):
        innovation = measurement - np.dot(self.measurement_matrix, self.state)
        innovation_covariance = np.dot(np.dot(self.measurement_matrix, self.covariance), self.measurement_matrix.T) + self.measurement_noise
        kalman_gain = np.dot(np.dot(self.covariance, self.measurement_matrix.T), inv(innovation_covariance))

        self.state = self.state + np.dot(kalman_gain, innovation)
        self.covariance = np.dot((np.eye(self.covariance.shape[0]) - np.dot(kalman_gain, self.measurement_matrix)), self.covariance)

        return self.state