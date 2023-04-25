import traci 
from traci._trafficlight import Logic , Phase 
from traci import trafficlight
from codes.Environment.traffic_light_actions import Actions


class traffic_light:
    
    def __init__(self ,id_traffic_light):
        self.id_traffic_light =  id_traffic_light
        self.queue_cmd = []
        self.default_program = '0'
        self.duration = 15

    ############# getters #######################
    def get_id(self):
        """ return id of traffic light signal """
        return self.id_traffic_light
    
    def get_current_state(self):
        """ return state (string) like 'GGrrGGrr' """
        return trafficlight.getRedYellowGreenState(self.id_traffic_light)
    
    def get_current_phase(self):
        """ return the index of the current phase """
        return trafficlight.getPhase(self.id_traffic_light)

    def get_current_program(self):
        """ return the id of the current program """
        return trafficlight.getProgram(self.id_traffic_light)
    def get_NS_index_phase(self):
         # get intex phases in the current program:
        if self.get_current_program() == '0':
            return 0 
        else: 
            return 0

    def get_EW_index_phase(self):
         # get intex phases in the current program:
        if self.get_current_program() == '0':
            return 2
        else:
            return 1
        
    def get_current_action(self):
        """ return the current action like { Actions.N_S_open  }"""

        if self.get_current_state() == 'GGGGGGGG':
            return Actions.All_green
        elif self.get_current_state() == 'rrrrrrrr':
            return Actions.All_red
        # elif self.get_current_program() == self.default_program:
        elif self.get_current_phase() == self.get_NS_index_phase() :
            return Actions.N_S_open
        elif self.get_current_phase() == self.get_EW_index_phase():
            return Actions.E_W_open
        else:
            return Actions.Switch_phase


    ########### control of traffic light signal ###################
    def reset_control_trafficlight(self):
        """ return the traffic light to default program """
        traci.trafficlight.setProgram(self.id_traffic_light , self.default_program)

    def set_phase(self , index_phase):
        """ change the current phase to passed phase """
        traci.trafficlight.setPhase(self.get_id() , index_phase) 

    def add_program(self ,id_program,states ,durations):
        """ 
        add new program to programs of traffic light signal 
        param id_program: id of new program 
        param states: list of states for phases 
        param durations: list of durations for phases 
        """
        phases = []
        for i in range(len(states)):
            phases.append(Phase(durations[i] , states[i]))

        program = Logic(id_program,0,0,phases)
        traci.trafficlight.setProgramLogic(self.id_traffic_light ,program)

    def Switches_to_program(self,id_program):
        """ Switches to the program with the given programID. """
        traci.trafficlight.setProgram(self.id_traffic_light , id_program)


    def can_change_phase(self ,step):
        """ return True if duration of the current phase is finished else False"""

        NextSwitch = trafficlight.getNextSwitch(self.id_traffic_light)
        rest_time = NextSwitch - step

        if self.get_current_action() != Actions.Switch_phase:
            return False
        
        elif self.get_current_action() == Actions.Switch_phase and rest_time <=0:
            return True
        else:
            return False
        
    def Add_cmd (self ,action):
        """ 
        add action to queue cmd to execute if that possible
        action: is contains item of traffic light actions 
        """
        self.queue_cmd.append(action)

    def check_cmds_to_execute(self):
        """ check if queue cmd contains actions or not and if it have actions to execute """
        if len(self.queue_cmd)<1:
            pass

        else:
            self.execute_cmd()

    def execute_cmd(self):
        """ check if action execute already or execute action of traffic light and remove from queue """
        action = self.queue_cmd[0]
        step = traci.simulation.getTime()
        is_can_switch = self.can_change_phase(step)
        remove_action = False
        # print('id_traffic_light: {} in step {} action {} is executed'.format(self.id_traffic_light,step,action))
        self.apply_action(action)
        remove_action = True

        ### the old code we will reused don't remve this code ############################
        # if (action == self.get_current_action()):
        #     remove_action = False

        
        # elif is_can_switch:
        #     self.apply_action(action)
        #     remove_action = True
        # else:
        #     pass # don't work anything
        # else:
        #     self.apply_action(action)
        #     remove_action = True
        #################################################################################

        if remove_action:
            self.queue_cmd.pop(0)

    def apply_action(self, action):
        """ apply the action on traffic light """

        ### this part of code will reused after solve some bags ####################################
        # reset traffic light to default program if it is not in default program
        # if self.get_current_program() != '0':
        #     self.reset_control_trafficlight() # Reset the traffic light control
        # # set traffic lights for north-south direction
        # if action == Actions.N_S_open:
        #     if self.get_current_phase() == 0 :
        #         pass # if the current phase is already green for north-south direction, do nothing
            
        #     else:
        #         self.set_phase(0) # if the current phase is not green for north-south direction, set it to green
        
        # if action == Actions.E_W_open:
        #     if self.get_current_phase() == 2:
        #         pass # if the current phase is already green for east-west direction, do nothing
            
        #     else:self.set_phase(2)
        #############################################################################################

        if self.get_current_program() == '0':
            # add new program to traffic light 
            all_program_logics = traci.trafficlight.getAllProgramLogics(self.id_traffic_light)
            program_0 = all_program_logics[0]
            phases = program_0.phases
            s_n_phase = phases[0].state
            e_w_phase = phases[2].state
            new_program_states = [s_n_phase , e_w_phase]
            durations_sn = phases[0].duration
            durations_EW = phases[2].duration

            new_program_durations = [self.duration , self.duration]

            self.add_program(
                id_program= '1' , 
                states= new_program_states, 
                durations=new_program_durations)

       
        

        # set traffic lights for north-south direction
        if action == Actions.N_S_open:

            self.set_phase(self.get_NS_index_phase()) # if the current phase is not green for north-south direction, set it to green

            # if self.get_current_phase() == self.get_NS_index_phase() :
            #     pass # if the current phase is already green for north-south direction, do nothing
            
            # else:
            #     self.set_phase(self.get_NS_index_phase()) # if the current phase is not green for north-south direction, set it to green
        
        if action == Actions.E_W_open:
            self.set_phase(self.get_EW_index_phase())
            # if self.get_current_phase() == self.get_EW_index_phase():
            #     pass # if the current phase is already green for east-west direction, do nothing
            
            # else:self.set_phase(self.get_EW_index_phase())

    def apply_all_green(self):
        """
        apply all lanes of intersection is open 
        this function we will remove if we not use it
        """
        duration,new_state = 30,''  # duration for green light
        for i in range(len(state)):new_state+='G'
        state = new_state
        states = [state]
        durations = [duration]
        self.add_program('1' , states ,durations)
        self.Switches_to_program('1')