import numpy as np
import math

class VehicleStabilityAnalyzer:
    def __init__(self, 
                 sampling_rate=20,  # Hz
                 stability_window=3.0  # seconds of historical data
                ):
        """
        Vehicle Stability and Driver Attention Monitoring System
        
        Parameters:
        - sampling_rate: Data sampling frequency in Hz
        - stability_window: Historical data window for analysis
        """
        self.sampling_rate = sampling_rate
        self.stability_window = stability_window
        
        # Stability thresholds
        self.stability_thresholds = {
            'yaw_rate_critical': math.radians(20),  # Critical yaw rate
            'steering_rate_critical': math.radians(30),  # Critical steering rate
            'lateral_acceleration_critical': 3.0,  # m/s²
            'combined_instability_threshold': 0.7  # Combined instability score
        }
        
        # Data storage
        self.data_history = {
            'yaw_rate': [],
            'steering_angle': [],
            'lateral_acceleration': []
        }
        
        # Statistical trackers
        self.stability_metrics = {
            'yaw_rate_variance': 0,
            'steering_rate_variance': 0,
            'lateral_acceleration_variance': 0
        }
    
    def update_sampling_rate(self, new_sampling_rate):
        """
        Dynamically update sampling rate
        
        Parameters:
        - new_sampling_rate: New sampling frequency in Hz
        """
        self.sampling_rate = new_sampling_rate
        # Adjust data history window based on new sampling rate
        max_history_length = int(self.stability_window * new_sampling_rate)
        
        # Trim existing history if needed
        for key in self.data_history:
            self.data_history[key] = self.data_history[key][-max_history_length:]
    
    def add_vehicle_data(self, yaw_rate, steering_angle, lateral_acceleration):
        """
        Add new vehicle data point for stability analysis
        
        Parameters:
        - yaw_rate: Current yaw rate (rad/s)
        - steering_angle: Current steering angle (rad/s)
        - lateral_acceleration: Current lateral acceleration (m/s²)
        """
        # Maintain maximum window size
        max_history_length = int(self.stability_window * self.sampling_rate)

        self.data_history['yaw_rate'] = yaw_rate
        self.data_history['steering_angle'] = steering_angle
        self.data_history['lateral_acceleration'] = lateral_acceleration

        # # Add new data points
        # self._append_with_limit(self.data_history['yaw_rate'], yaw_rate, max_history_length)
        # self._append_with_limit(self.data_history['steering_angle'], steering_angle, max_history_length)
        # self._append_with_limit(self.data_history['lateral_acceleration'], lateral_acceleration, max_history_length)
    
    def _append_with_limit(self, data_list, new_value, max_length):
        """
        Append new value to list while maintaining maximum length
        """
        data_list.append(new_value)
        if len(data_list) > max_length:
            data_list.pop(0)
    
    def calculate_stability_metrics(self):
        """
        Calculate stability metrics from historical data
        
        Returns:
        - Comprehensive stability assessment
        """
        # Compute variances and statistical measures
        stability_assessment = {
            'yaw_rate': self._analyze_metric(
                self.data_history['yaw_rate'], 
                self.stability_thresholds['yaw_rate_critical']
            ),
            'steering_angle': self._analyze_metric(
                self.data_history['steering_angle'], 
                self.stability_thresholds['steering_rate_critical']
            ),
            'lateral_acceleration': self._analyze_metric(
                self.data_history['lateral_acceleration'], 
                self.stability_thresholds['lateral_acceleration_critical']
            )
        }
        
        # Combined instability score
        combined_instability = self._calculate_combined_instability(stability_assessment)
        
        return {
            'stability_metrics': stability_assessment,
            'combined_instability_score': combined_instability,
            'driver_alert': self._generate_driver_alert(combined_instability)
        }
    
    def _analyze_metric(self, data, critical_threshold):
        """
        Analyze individual metric for instability
        
        Parameters:
        - data: List of historical data points
        - critical_threshold: Threshold for instability
        
        Returns:
        - Instability assessment for the metric
        """
        if not data:
            return {'instability': 0, 'variance': 0}
        
        # Calculate variance and peak values
        variance = np.var(data)
        peak_value = max(abs(np.max(data)), abs(np.min(data)))
        
        # Normalize instability
        instability = min(1, peak_value / critical_threshold)
        
        return {
            'instability': instability,
            'variance': variance,
            'peak_value': peak_value
        }
    
    def _calculate_combined_instability(self, stability_assessment):
        """
        Calculate overall vehicle instability score
        
        Parameters:
        - stability_assessment: Dictionary of individual metric assessments
        
        Returns:
        - Combined instability score (0-1)
        """
        # Weight different metrics
        weights = {
            'yaw_rate': 0.4,
            'steering_angle': 0.3,
            'lateral_acceleration': 0.3
        }
        
        combined_score = sum(
            stability_assessment[metric]['instability'] * weights[metric]
            for metric in weights
        )
        
        return combined_score
    
    def _generate_driver_alert(self, combined_instability):
        """
        Generate driver alert based on instability score
        
        Parameters:
        - combined_instability: Overall instability score (0-1)
        
        Returns:
        - Alert message and severity
        """
        alerts = [
            {
                'threshold': 0.2,
                'severity': 'LOW',
                'message': "Normal driving conditions"
            },
            {
                'threshold': 0.5,
                'severity': 'MEDIUM',
                'message': "CAUTION: Maintain steady driving"
            },
            {
                'threshold': 0.7,
                'severity': 'HIGH',
                'message': "URGENT: Reduce speed and focus"
            },
            {
                'threshold': 1.0,
                'severity': 'CRITICAL',
                'message': "EMERGENCY: Pull over safely immediately!"
            }
        ]
        
        # Find appropriate alert
        for alert in alerts:
            if combined_instability <= alert['threshold']:
                return {
                    'severity': alert['severity'],
                    'message': alert['message'],
                    'instability_score': combined_instability
                }
        
        # Fallback
        return {
            'severity': 'CRITICAL',
            'message': "EMERGENCY: Extreme driving instability detected",
            'instability_score': combined_instability
        }