import Tkinter as Tk
import os
import subprocess
import threading
from time import sleep


#def h(event):
#   print 'panic'
#Taken liberally from https://stackoverflow.com/
#questions/26211821/partial-read-from-stdout-on-python-using-popen
#User: mrad
PSCF_PATH = 'pscf'
MATLAB = '/Applications/MATLAB_R2015b.app/bin/matlab'
model_flag = False

class Slave_process(threading.Thread):
   def __init__(self):
            threading.Thread.__init__(self)
            self.daemon = True
            self.buffer = ''
            self.bufLock = threading.Lock()

   def run(self):
      global PSCF_PATH
      cmd = PSCF_PATH + ' < param'
      monkey = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)

      while monkey.poll() is None:
            data = monkey.stdout.readline(4)
            if data !="":
                  with self.bufLock:
                        self.buffer += data

   def get_output(self):
      with self.bufLock:
            buf = self.buffer
            self.buffer = ''
            return buf

def read_da_file(run_msg, child):
      #print "read_da_damn_file"
      data = child.get_output()
      run_msg.insert(Tk.INSERT, data)
      if child.is_alive():
            root.after(1000, read_da_file,run_msg,child)
      else:
            child.join()

def make_input():
      with open('param', 'w') as f:
            f.write(' format 1 0\n\n')
            f.write('MONOMERS\nN_monomer\n\t\t\t\t'+(mainPage.N_mon.get())+'\n')

            string = 'kuhn\n'
            for i in mainPage.kuhn.kuhn_list:
                  string += str(i.get()) + '\t'
            string += '\n\n'
            f.write( string)

            f.write('CHAINS\nN_chain\n'+str(mainPage.N_chain.get())+'\n')
            string = 'N_block\n'
            for i in range(int(mainPage.N_chain.get())):
               string += mainPage.chain.nblock_list[i].get() + '\n'
            f.write(string)

            string = 'block_monomer\n'
            for i in range(int(mainPage.N_chain.get())):
               for j in range(int(mainPage.chain.nblock_list[i].get())):
                  string +='\t\t' + str(mainPage.chain.block_monomer[i][j].get()) +'\t\t'
               string +='\n'  
            f.write(string)

            string = 'block_length\n'
            for i in range(int(mainPage.N_chain.get())):
               for j in range(int(mainPage.chain.nblock_list[i].get())):
                  string +='\t\t' + str(mainPage.chain.block_length[i][j].get()) +'\t\t'
               string +='\n'  
            string +='\n'
            f.write(string)

            f.write('COMPOSITION\nensemble\n\t\t\t\t' + str(mainPage.Ensemble.get()) + '\n' )
            #phi
            string ='phi\n\t'
            for i in mainPage.phi.phi_list:
                  string += str(i.get()) + '\t'
            string +='\n\n'
            f.write(string)

            f.write('INTERACTION\ninteraction_type\n\t'+"'" + str(mainPage.interaction_type.get()) 
                  +"'\n")

            if str(mainPage.interaction_type.get()) == "chi":
                  f.write('chi')
                  for i in range(int(mainPage.N_mon.get())):
                        for j in range(i):
                              f.write(str(mainPage.chi.chi_list[i][j].get()) + '\t')
                        f.write('\n')
                  f.write('\n')

            f.write('UNIT_CELL\ndim\n\t'+str(mainPage.dimension.get())+'\n')
            f.write('crystal_system\n\t'+"'"+str(mainPage.crystal_type.get())+"'"+'\n')

            f.write('N_cell_param\n\t'+str(mainPage.N_cell_param.get())+'\n')
            string = 'cell_param\n\t'
            for i in mainPage.cell_param.cell_list:
                  string += str(i.get()) + '\t'
            string += '\n\n'  
            f.write(string)

            #ngrid
            string = 'DISCRETIZATION\nngrid\n\t'
            for i in range(int(mainPage.dimension.get())):
                  string += str(mainPage.ngrid.grid_list[i].get()) +  '\t'
            string +='\n'
            f.write(string)

            f.write('chain_step\n\t' + str(mainPage.Chain_step.get()) + '\n\n')
            f.write('BASIS\ngroup_name\n\t' + "'"+str(mainPage.Group_name.get())+"'"+"\n\n")

            global model_flag
            if model_flag == True:
               f.write('KGRID_TO_RGRID\ninput_filename\n\t\t'+"'rho_kgrid'\n")
               f.write('output_filename\n\t\t\t' + "'rho_rgrid'\n\n")
               f.write('RGRID_TO_FIELD\ninput_filename\n\t\t'+"'rho_rgrid'\n")
               f.write('output_filename\n\t\t' + "'rho'\n\n")
               f.write('RHO_TO_OMEGA\ninput_filename\n\t\t'+"'rho'\n")
               f.write('output_filename\n\t\t\t' + "'in.omega'\n\n")

            f.write("ITERATE\ninput_filename\n" + str("'in.omega'") +'\n')
            f.write("output_prefix\n\t"+str("'out/'")+'\n')
            f.write("max_itr\n\t\t\t"+str(200)+'\n')
            f.write("error_max\n\t"+str(1.00000E-05)+'\n')
            f.write("domain\n\t"+str("F")+'\n')
            f.write("itr_algo\n"+"'"+str('AM')+"'"+'\n')
            f.write("N_hist\n\t"+str(40)+'\n\n')
            f.write("FINISH")

def make_model():
      with open('model', 'w') as f:
            f.write(' format 1 0\n\n')
            f.write('MONOMERS\nN_monomer\n\t\t\t\t'+(mainPage.N_mon.get())+'\n\n')

            f.write('CHAINS\n')
            string = 'N_block\n'
            for i in range(int(mainPage.N_chain.get())):
               string += mainPage.chain.nblock_list[i].get() + '\n'
            f.write(string)

            string = 'block_length\n'
            for i in range(int(mainPage.N_chain.get())):
               for j in range(int(mainPage.chain.nblock_list[i].get())):
                  string +='\t\t' + str(mainPage.chain.block_length[i][j].get()) +'\t\t'
               string +='\n'  
            string +='\n'
            f.write(string)

            f.write('UNIT_CELL\ndim\n\t'+str(mainPage.dimension.get())+'\n')
            f.write('crystal_system\n\t'+"'"+str(mainPage.crystal_type.get())+"'"+'\n')

            f.write('N_cell_param\n\t'+str(mainPage.N_cell_param.get())+'\n')
            string = 'cell_param\n\t'
            for i in mainPage.cell_param.cell_list:
                  string += str(i.get()) + '\t'
            string += '\n\n'  
            f.write(string)

            #ngrid
            string = 'DISCRETIZATION\nngrid\n\t'
            for i in range(int(mainPage.dimension.get())):
                  string += str(mainPage.ngrid.grid_list[i].get()) +  '\t'
            string +='\n\n'
            f.write(string)

            f.write('BASIS\ngroup_name\n\t' + "'"+str(mainPage.Group_name.get())+"'"+"\n\n")

            f.write('output_filename\n\t\t\t'+"'rho_kgrid'\n\n")
            f.write("PARTICLES\nN_particles\n" + str(mainPage.dialog.E1.get()) + "\n")
            f.write("Fractional_coordinates\n")
            string_list = str(mainPage.dialog.E2.get()).split(';')
            for i in string_list:
               f.write(i + '\n')
            f.write('\nFINISH\n')


def sample_run(run_msg):
      make_input()
      data = ''
      child = Slave_process()
      child.start()
      read_da_file(run_msg, child)
      #subprocess.call(["pscf", "<","param"], shell=True)
      #subprocess.call(["pscf < param"], shell=True)

# def read_da_file(run_msg, monkey):
#       root.update()
#       for lines in monkey.stdout:
#             run_msg.insert(Tk.INSERT, lines)
#       if monkey.poll() == None:
#             root.after(1000, read_da_file, run_msg, monkey)

# def sample_run(run_msg):
#       monkey = subprocess.Popen(["pscf < param"], stdout=subprocess.PIPE, shell=True)
#       root.after(1000, read_da_file, run_msg, monkey)
            

class DialogBox(Tk.Toplevel):
   def __init__(self, parent):
      Tk.Toplevel.__init__(self,parent)
      self.body = Tk.Frame(self)
      self.body.grid(row=0)
      self.grab_set()

      Tk.Label(self.body, text="N_particles").grid(row=0)
      self.E1 = Tk.Entry(self.body, width=10)
      self.E1.grid(row=1)
      Tk.Label(self.body, text="Fractional Coordinates").grid(row=2)
      self.E2 = Tk.Entry(self.body, width=10)
      self.E2.grid(row=3, columnspan=3, rowspan=3, sticky=Tk.NW +Tk.SE)
      b = Tk.Button(self.body, text="Close", command=self.ok)
      b.grid(row=7,column=0)
      b2 = Tk.Button(self.body, text="Generate File", command=self.run)
      b2.grid(row=7,column=1)
   def ok(self):
      self.destroy()
   def run(self):
      make_model()
      global MATLAB
      cmd = MATLAB + ' -nodisplay -nojvm -nosplash -r' + " 'density_BCC;exit'"
      haha= subprocess.Popen([cmd],shell=True)
      global model_flag
      model_flag = True





class Chain(Tk.Frame):
   def __init__(self,master):
      Tk.Frame.__init__(self,master)
      Tk.Label(self, text="N_block").grid(row=0)
      Tk.Label(self, text="block_monomer").grid(row=1)
      self.bl_label = Tk.Label(self, text="block_length")

      self.nblock_list = []
      self.nblock_option = []
      self.block_monomer = []
      self.block_length = []

   def __clean(self):
      for inner in self.block_length:
         for j in inner:
            j.destroy()
      del self.block_length[:]

      for inner in self.block_monomer:
         for j in inner:
            j.destroy()
      del self.block_monomer[:]

      del self.nblock_list[:]
      for j in self.nblock_option:
         j.destroy()
      del self.nblock_option[:]

   def __make_chain(self, N_chain):
      for i in range(N_chain):
         self.block_monomer.append([])
         for j in range(int(self.nblock_list[i].get())):
            self.block_monomer[i].append(Tk.Entry(self, width=10))
            self.block_monomer[i][j].grid(row=1 + i,column=j+1)

      for i in range(N_chain):
         self.block_length.append([])
         for j in range(int(self.nblock_list[i].get())):
            self.block_length[i].append(Tk.Entry(self, width = 10))
            self.block_length[i][j].grid(row=2+N_chain+i, column=j+1)

   def __update_block(self, N_chain):
      for inner in self.block_length:
         for j in inner:
            j.destroy()
      del self.block_length[:]

      for inner in self.block_monomer:
         for j in inner:
            j.destroy()
      del self.block_monomer[:]
      self.__make_chain(N_chain)

   def make(self, N_chain):
      self.__clean()
      self.bl_label.grid_forget()
      self.bl_label.grid(row=2+N_chain)
      optionList = ("1","2","3","4")
      for i in range(N_chain):
         self.nblock_list.append(Tk.StringVar())
         self.nblock_list[i].set(optionList[1])
         self.nblock_option.append(Tk.OptionMenu(self, self.nblock_list[i], *optionList, command=lambda x: self.__update_block(N_chain)))
         self.nblock_option[i].grid(row=0, column=i+1)
      self.__make_chain(N_chain)



class Kuhn(Tk.Frame):
   def __init__(self, master):
      Tk.Frame.__init__(self, master)
      self.kuhn_list = []
   def make(self, length):
      for i in self.kuhn_list:
            i.destroy()
      del self.kuhn_list[:]
      for i in range(length):
            self.kuhn_list.append(Tk.Entry(self, width=10))
            self.kuhn_list[i].grid(row=0, column = i)

class Ngrid(Tk.Frame):
   def __init__(self, master):
      Tk.Frame.__init__(self,master)
      self.grid_list = []
   def make(self, length):
      for i in self.grid_list:
            i.destroy()
      del self.grid_list[:]
      for i in range(length):
            self.grid_list.append(Tk.Entry(self, width = 10))
            self.grid_list[i].grid(row=0, column = i)

class Cell_param(Tk.Frame):
   def __init__(self, master):
      Tk.Frame.__init__(self,master)
      self.cell_list = []
   def make(self, length):
      for i in self.cell_list:
            i.destroy()
      del self.cell_list[:]
      for i in range(length):
            self.cell_list.append(Tk.Entry(self, width = 10))
            self.cell_list[i].grid(row=0, column = i)

class Chi(Tk.Frame):
   def __init__(self,master):
      Tk.Frame.__init__(self, master)
      self.chi_list = []
      self.chi_A = []
      self.chi_B = []
      self.temp = None
      self.labels = []

   def __clean(self):
      for inner in self.chi_list:
            for j in inner:
                  j.destroy()
      del self.chi_list[:]
      for inner in self.chi_A:
            for j in inner:
                  j.destroy()
      del self.chi_A[:]
      for inner in self.chi_B:
            for j in inner:
                  j.destroy()
      del self.chi_B[:]
      if self.temp is not None:
            self.temp.destroy()
            self.temp = None
      for label in self.labels:
            label.destroy()
      del self.labels[:]

   def make(self, length, type):
      self.__clean()
      if type == "chi":
            self.labels.append(Tk.Label(self, text= "chi"))
            self.labels[0].grid(row=0, column = 0)
            for i in range(length):
                  self.chi_list.append([])
                  for j in range(i):
                        self.chi_list[i].append(Tk.Entry(self, width = 10))
                        self.chi_list[i][j].grid(row=i, column = j+1)
      else:
            self.labels.append(Tk.Label(self, text= "chi_A"))
            self.labels[0].grid(row=0, column = 0)
            for i in range(length):
                  self.chi_A.append([])
                  for j in range(i):
                        self.chi_A[i].append(Tk.Entry(self, width = 10))
                        self.chi_A[i][j].grid(row=i, column = j+1)
            
            self.labels.append(Tk.Label(self, text= "chi_B"))
            self.labels[1].grid(row=length, column = 0)    
            for i in range(length):
                  self.chi_B.append([])
                  for j in range(i):
                        self.chi_B[i].append(Tk.Entry(self, width = 10))
                        self.chi_B[i][j].grid(row=i+(length-1), column = j+1)

            self.labels.append(Tk.Label(self, text= "Temp"))
            self.labels[2].grid(row=(length*2), column = 0)
            self.temp = Tk.Entry(self, width = 10)
            self.temp.grid(row=(length*2), column = 1)

class Phi(Tk.Frame):
   def __init__(self,master):
      Tk.Frame.__init__(self,master)
      self.phi_list = []
   def make(self,N_chain):
      for i in self.phi_list:
         i.destroy()
      del self.phi_list[:]
      for i in range(N_chain):
         self.phi_list.append(Tk.Entry(self,width= 10))
         self.phi_list[i].grid(row=0, column = i)

class MainPage():
   def __init__(self, master, title = None):
      pass

   # def delete_grid(self, dimension_old):
   #    if self.dimension_old.get() == "3":
   #          self.e3.destroy()
   #          self.e4.destroy()
   #          self.e5.destroy()
   #    elif self.dimension_old.get() == "1":
   #          self.e3.destroy()

   def spawn_wizard(self, root):
      self.dialog = DialogBox(root)
      root.wait_window(self.dialog)

   def update_dim(self, event):
      self.ngrid.make(int(self.dimension.get()))

   def update_mon(self, event):
      self.kuhn.make(int(self.N_mon.get()))
      self.chi.make(int(self.N_mon.get()), str(self.interaction_type.get()))

   def update_chi(self, event):
      self.chi.make(int(self.N_mon.get()), str(self.interaction_type.get()))

   def update_cell(self, event):
      self.cell_param.make(int(self.N_cell_param.get()))

   def update_Nchain(self,event):
      self.chain.make(int(self.N_chain.get()))
      self.phi.make(int(self.N_chain.get()))
   # def draw_grid(self, event):
   #    if self.dimension.get() == "3":
   #          self.delete_grid(self.dimension_old)
   #          self.e3 = Tk.Entry(self.body, width = 6)
   #          self.e3.grid(row=3, column=1)
   #          self.e4 = Tk.Entry(self.body, width = 6)
   #          self.e4.grid(row=3, column=2)
   #          self.e5 = Tk.Entry(self.body, width = 6)
   #          self.e5.grid(row=3, column=3)
   #          self.dimension_old = self.dimension
   #    elif self.dimension.get() == "1":
   #          self.delete_grid(self.dimension_old)
   #          self.e3 = Tk.Entry(self.body, width = 21)
   #          self.e3.grid(row=3, column=1, columnspan = 3)
   #          self.dimension_old = self.dimension

   # def draw_dim(self):
   #    if self.dimension.get() == "3":
   #          self.e3 = Tk.Entry(self.body, width = 6)
   #          self.e3.grid(row=12, column=1)
   #          self.e4 = Tk.Entry(self.body, width = 6)
   #          self.e4.grid(row=12, column=2)
   #          self.e5 = Tk.Entry(self.body, width = 6)
   #          self.e5.grid(row=12, column=3)
   #    elif self.dimension.get() == "1":
   #          self.e3 = Tk.Entry(self.body, width = 21)
   #          self.e3.grid(row=12, column=1, columnspan = 3)

   def makeframe(self, master,title = None):
      self.body = Tk.Frame(master, height = 600, width = 600)
      #self.body.bind('<<panic>>', h)
      self.body.grid(row=0,sticky="nsew")
      self.body.winfo_toplevel().title("PSCF")


      Tk.Label(self.body, text= "N_monomer").grid(row=0)
      optionList = ("1","2","3","4")
      self.N_mon = Tk.StringVar()
      self.N_mon.set(optionList[1])
      Tk.OptionMenu(self.body, self.N_mon, *optionList, command=self.update_mon).grid(row=0,column=1,columnspan = 3,sticky=Tk.E+Tk.W)

      Tk.Label(self.body, text= "Kuhn").grid(row=1)
      self.kuhn = Kuhn(self.body)
      self.kuhn.make(int(self.N_mon.get()))
      self.kuhn.grid(row=1, column =1)

      Tk.Label(self.body, text= "N_chain").grid(row=2)
      optionList = ("1","2","3","4")
      self.N_chain = Tk.StringVar()
      self.N_chain.set(optionList[0])
      Tk.OptionMenu(self.body, self.N_chain, *optionList, command=self.update_Nchain).grid(row=2,column=1,columnspan = 3, sticky=Tk.E+Tk.W)
      self.chain = Chain(self.body)
      self.chain.make(int(self.N_chain.get()))
      self.chain.grid(row=3, column = 1)

      Tk.Label(self.body, text= "Ensemble").grid(row=4)
      self.Ensemble = Tk.Entry(self.body, width = 21)
      self.Ensemble.grid(row=4, column=1, columnspan =3)

      Tk.Label(self.body, text="phi").grid(row=5)
      self.phi = Phi(self.body)
      self.phi.make(int(self.N_chain.get()))
      self.phi.grid(row=5, column = 1)
      
      #INTERACTION
      Tk.Label(self.body, text="interaction_type").grid(row=6)
      optionList = ("chi", "chi_T")
      self.interaction_type = Tk.StringVar()
      self.interaction_type.set(optionList[0])
      Tk.OptionMenu(self.body, self.interaction_type, *optionList, command=self.update_chi).grid(row=6, column=1, columnspan=3)

      self.chi = Chi(self.body)
      self.chi.make(int(self.N_mon.get()), str(self.interaction_type.get()))
      self.chi.grid(row=7)
      # Tk.Label(self.body, text="chi").grid(row=7)
      # self.chi = Tk.Entry(self.body, width = 21)
      # self.chi.grid(row=7, column=1, columnspan = 3)

      optionList = ("1","2","3")
      self.dimension = Tk.StringVar()
      self.dimension.set(optionList[2])
      Tk.Label(self.body, text="dimension").grid(row=8)
      Tk.OptionMenu(self.body, self.dimension, *optionList, command=self.update_dim).grid(row=8, column = 1)

      Tk.Label(self.body, text="crystal_system").grid(row=9)
      optionList = ("cubic", "tetragonal", "orthorhombic")
      self.crystal_type = Tk.StringVar()
      self.crystal_type.set(optionList[0])
      Tk.OptionMenu(self.body, self.crystal_type, *optionList).grid(row=9, column=1, columnspan = 3, sticky=Tk.E+Tk.W)


      Tk.Label(self.body, text="N_cell_param").grid(row=10)
      optionList = ("1","2","3","4","5","6")
      self.N_cell_param = Tk.StringVar()
      self.N_cell_param.set(optionList[0])
      Tk.OptionMenu(self.body, self.N_cell_param, *optionList, command=self.update_cell).grid(row=10, column=1)

      Tk.Label(self.body, text="Cell_param").grid(row=11)
      self.cell_param = Cell_param(self.body)
      self.cell_param.grid(row=11, column=1, columnspan = 3)
      self.cell_param.make(int(self.N_cell_param.get()))

      Tk.Label(self.body, text="Ngrid").grid(row=12)
      self.ngrid = Ngrid(self.body)
      self.ngrid.make(int(self.dimension.get()))
      self.ngrid.grid(row=12, column=1)

      Tk.Label(self.body, text="Chain_step").grid(row=13)
      self.Chain_step = Tk.Entry(self.body, width = 21)
      self.Chain_step.grid(row=13, column=1, columnspan =3)

      Tk.Label(self.body, text="Group_name").grid(row=14)
      self.Group_name = Tk.Entry(self.body, width = 21)
      self.Group_name.grid(row=14, column=1, columnspan =3)
      # e0 = Tk.Entry(self.body, width = 21).grid(row=2, column=1, columnspan = 3)

      # #self.body.event_add('<<panic>>')

      # self.dimension_old = self.dimension

      # self.e3 = Tk.Entry(self.body, width = 6)
      # self.e3.grid(row=3, column=1)
      # self.e4 = Tk.Entry(self.body, width = 6)
      # self.e4.grid(row=3, column=2)
      # self.e5 = Tk.Entry(self.body, width = 6)
      # self.e5.grid(row=3, column=3)



      # e0 = Tk.Entry(self.body, width = 21).grid(row=5, column=1, columnspan = 3)
      # e0 = Tk.Entry(self.body, width = 21).grid(row=6, column=1, columnspan = 3)
      self.run_msg = Tk.StringVar()
      b0 = Tk.Button(self.body, text = "Omega Wizard", bg = "gray", command=lambda: self.spawn_wizard(root)).grid(row=16)
      b0 = Tk.Button(self.body, text = "Run PSCF", bg = "gray", command=lambda: sample_run(self.M0)).grid(row=16, column=1)
      self.M0 = Tk.Text(self.body, relief = "sunken", height = 8, padx = 2, pady = 2, bd = 3)
      self.M0.grid(row=17, columnspan = 4, sticky=Tk.N+Tk.E+Tk.S+Tk.W)
      scroll_bar = Tk.Scrollbar(self.body, orient=Tk.VERTICAL, command=self.M0.yview)
      scroll_bar.grid(row=17,column = 4, sticky = Tk.N+Tk.S)
      self.M0['yscrollcommand'] = scroll_bar.set



root = Tk.Tk()
mainPage = MainPage(root)
mainPage.makeframe(root)
root.mainloop()
