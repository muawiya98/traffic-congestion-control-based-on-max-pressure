from codes.Environment.traffic_light_actions import Actions

class traffic_lights_controler:

    def __init__(self , traffic_light_signals):
        """
        ## traffic lights controler : 
        to control of all traffic light signals in simulation

        traffic_light_signals : list of object of traffic light 
        """
        self.control_msg = {}
        self.traffic_light_signals = traffic_light_signals
        self.traffic_light_signals_dic_actions = {}
        for tls_object in traffic_light_signals:
            self.traffic_light_signals_dic_actions[tls_object.get_id()] = None

    def set_control_msg(self , msg):
        """ set new control message """
        self.control_msg = msg

    def convert_msg_to_tls_cmd (self):
        """ 
        convert control message to message that traffic light signal understand
        """
        for key in self.control_msg.keys():
            if self.control_msg[key] == (1,0):
                self.traffic_light_signals_dic_actions[key] = Actions.N_S_open
            elif self.control_msg[key] == (0,1):
                self.traffic_light_signals_dic_actions[key] = Actions.E_W_open
            # else :
            #     self.traffic_light_signals_dic_actions[key] = None


    def send_Actions(self , msg):
        """ 
        msg: is dictionary contains keys is ids of tfs and values is action for each tfs

        """
        self.set_control_msg(msg)
        self.convert_msg_to_tls_cmd()
        for tls in self.traffic_light_signals:
            action = self.traffic_light_signals_dic_actions[tls.get_id()]
            tls.Add_cmd(action) 


