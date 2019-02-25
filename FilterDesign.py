import numpy as np
import scipy.signal as sc

class FIR_filter:
    def __init__(self, sampling_period, type, filter_order, analog_lower_cutoff_freq, analog_upper_cutoff_freq):
        self.Ts = sampling_period
        self.order = filter_order
        self.analog_lower_cutoff_freq = analog_lower_cutoff_freq
        self.analog_upper_cutoff_freq = analog_upper_cutoff_freq
        self.type = type
        self.filter_coeffs = []

        self.calculate_filter_coeffs()

    def calculate_filter_coeffs(self):
        if self.type == "Low Pass":
            self.filter_coeffs = sc.firwin(numtaps = self.order,
                                           cutoff = self.analog_lower_cutoff_freq,
                                           fs = 1/self.Ts
                                           )

        elif self.type == "High Pass":
            self.filter_coeffs = sc.firwin(numtaps = self.order,
                                           cutoff = self.analog_lower_cutoff_freq,
                                           fs = 1/self.Ts,
                                           pass_zero = False
                                           )

        elif self.type == "Band Pass":
            self.filter_coeffs = sc.firwin(numtaps = self.order,
                                           cutoff = [self.analog_lower_cutoff_freq, self.analog_upper_cutoff_freq],
                                           fs = 1/self.Ts,
                                           pass_zero = False
                                           )

        else:
            raise ValueError("Invalid filter type.")
            

    def apply(self, data):
        filtered_data = np.zeros(len(data))
        for i in range(self.order, len(data)):
            for k in range(self.order):
                filtered_data[i] += self.filter_coeffs[k]*data[i-k]

        return filtered_data[self.order:]



class IIR_filter:
    def __init__(self, P_order, P_coefficients, Q_order, Q_coefficients):
        self.P_order = P_order
        self.P_coeff = np.array(P_coefficients)
        self.Q_order = Q_order
        self.Q_coeff = np.array(Q_coefficients)

    def apply(self, data):
        n = len(data)
        filtered_data = np.zeros(n)
        lim = max(self.P_order, self.Q_order)

        for i in range(lim, n):

            """feedback filter"""
            for k in range(self.Q_order):
                filtered_data[i] -= self.Q_coeff[k]*filtered_data[i-k-1]

            """feedforward filter"""
            for k in range(self.P_order+1):
                filtered_data[i] += self.P_coeff[k]*data[i-k]

        return filtered_data[lim:]



class Butterworth_filter:
    def __init__(self, sampling_period, filter_order, analog_cutoff_freq, DC_Gain):
        self.Ts = sampling_period
        self.order = filter_order
        self.IIR_filters = [0]*int(np.ceil(self.order/2))
        self.cutoff_freq = analog_cutoff_freq
        self.DC_Gain = DC_Gain

        self.calculate_filter_coeffs()

    def calculate_filter_coeffs(self):
        digital_cutoff_angular_frequency = 2 * np.pi * self.cutoff_freq * self.Ts
        mapped_analog_cutoff_angular_frequency = 2 * np.tan(digital_cutoff_angular_frequency/2) / self.Ts

        butter_coeffs = [
                         [[1/mapped_analog_cutoff_angular_frequency]],

                         [[(1/mapped_analog_cutoff_angular_frequency)**2, 1.4142/mapped_analog_cutoff_angular_frequency]],

                         [[1/mapped_analog_cutoff_angular_frequency],
                          [(1/mapped_analog_cutoff_angular_frequency)**2, 1/mapped_analog_cutoff_angular_frequency]],

                         [[(1/mapped_analog_cutoff_angular_frequency)**2, 0.7654/mapped_analog_cutoff_angular_frequency],
                          [(1/mapped_analog_cutoff_angular_frequency)**2, 1.8478/mapped_analog_cutoff_angular_frequency]],

                         [[1/mapped_analog_cutoff_angular_frequency],
                          [(1/mapped_analog_cutoff_angular_frequency)**2, 0.6180/mapped_analog_cutoff_angular_frequency],
                          [(1/mapped_analog_cutoff_angular_frequency)**2, 1.6180/mapped_analog_cutoff_angular_frequency]],

                         [[(1/mapped_analog_cutoff_angular_frequency)**2, 0.5176/mapped_analog_cutoff_angular_frequency],
                          [(1/mapped_analog_cutoff_angular_frequency)**2, 1.4142/mapped_analog_cutoff_angular_frequency],
                          [(1/mapped_analog_cutoff_angular_frequency)**2, 1.9319/mapped_analog_cutoff_angular_frequency]],

                         [[1/mapped_analog_cutoff_angular_frequency],
                          [(1/mapped_analog_cutoff_angular_frequency)**2, 0.4450/mapped_analog_cutoff_angular_frequency],
                          [(1/mapped_analog_cutoff_angular_frequency)**2, 1.2470/mapped_analog_cutoff_angular_frequency],
                          [(1/mapped_analog_cutoff_angular_frequency)**2, 1.8019/mapped_analog_cutoff_angular_frequency]],

                         [[(1/mapped_analog_cutoff_angular_frequency)**2, 0.3902/mapped_analog_cutoff_angular_frequency],
                          [(1/mapped_analog_cutoff_angular_frequency)**2, 1.1111/mapped_analog_cutoff_angular_frequency],
                          [(1/mapped_analog_cutoff_angular_frequency)**2, 1.6629/mapped_analog_cutoff_angular_frequency],
                          [(1/mapped_analog_cutoff_angular_frequency)**2, 1.9616/mapped_analog_cutoff_angular_frequency]],
                        ]

        """N-th order butterworth is made by connecting multiple 1st/2nd order filters, in series"""
        if self.order%2 == 0:
            index = self.order - 1
            for i in range(len(self.IIR_filters)):
                P_coeff, Q_coeff = self.second_order_coeffs(butter_coeffs[index][i], self.Ts, self.DC_Gain if i == 0 else 1)
                self.IIR_filters[i] = IIR_filter(P_order = 2,
                                                 P_coefficients = P_coeff,
                                                 Q_order = 2,
                                                 Q_coefficients = Q_coeff)

        else:
            index = self.order - 1
            P_coeff, Q_coeff = self.first_order_coeffs(butter_coeffs[index][0], self.Ts, self.DC_Gain)
            self.IIR_filters[0] = IIR_filter(P_order = 1,
                                             P_coefficients = P_coeff,
                                             Q_order = 1,
                                             Q_coefficients = Q_coeff)

            for i in range(1, len(self.IIR_filters)):
                P_coeff, Q_coeff = self.second_order_coeffs(butter_coeffs[index][i], self.Ts, 1)
                self.IIR_filters[i] = IIR_filter(P_order = 2,
                                                 P_coefficients = P_coeff,
                                                 Q_order = 2,
                                                 Q_coefficients = Q_coeff)


    def apply(self, data):
        filtered_data = np.array(data)

        for filter in self.IIR_filters:
            filtered_data = filter.apply(filtered_data)

        return filtered_data

    def first_order_coeffs(self, butter_coeffs, T, Gain):
        P_coeff = np.zeros(2)
        Q_coeff = np.zeros(1)

        P_coeff[0] = Gain*T/(2*butter_coeffs[0] + T)
        P_coeff[1] = P_coeff[0]
        Q_coeff[0] = (-2*butter_coeffs[0]+T)/(2*butter_coeffs[0]+T)

        return P_coeff, Q_coeff

    def second_order_coeffs(self, butter_coeffs, T, Gain):
        P_coeff = np.zeros(3)
        Q_coeff = np.zeros(2)

        P_coeff[0] = Gain*T*T / (4*butter_coeffs[0] + 2*butter_coeffs[1]*T + T**2)
        P_coeff[1] = 2*Gain*T*T / (4*butter_coeffs[0] + 2*butter_coeffs[1]*T + T**2)
        P_coeff[2] = Gain*T*T / (4*butter_coeffs[0] + 2*butter_coeffs[1]*T + T**2)

        Q_coeff[0] = (-8*butter_coeffs[0] + 2*T*T) / (4*butter_coeffs[0] + 2*butter_coeffs[1]*T + T**2)
        Q_coeff[1] = (4*butter_coeffs[0] -2*butter_coeffs[1]*T + T**2) / (4*butter_coeffs[0] + 2*butter_coeffs[1]*T + T**2)

        return P_coeff, Q_coeff
