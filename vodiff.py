
# need the following libraries for the script to work correctly
import glob
import scipy.io
import pandas as pd
import os

# define a class to aggregate all of the PANODE data from RCVR testing
class AggregateAllPANODEData:
    
    # determine the initial variables needed to make this script work
    def __init__ (self):
        self.wildcardpath="C:\\path_to_logfile\\PANODE-*.mat"
        self.excelSavePath="C:\\somewhere_to_place_report\\MinedData.xlsx"
        self.fileslist=[]

    # recursive search for all files that match the wildcard path. Return the filepaths found
    def find_all_PANODE_mat_files(pth,list):
        for name in glob.glob(pth): 
            list.append(name)      
        return list

    # find all of the files wilth wildcard path used
    def listnames(self):
        filesFound=AggregateAllPANODEData.find_all_PANODE_mat_files(self.wildcardpath,self.fileslist)
        minedData=AggregateAllPANODEData.open_panode_mat_file_and_get_data(filesFound)
        AggregateAllPANODEData.create_excel_table_for_data(self,minedData)
        
    # open all of the files that have been found
    def open_panode_mat_file_and_get_data(fileslist):
        # introduce a simple counter
        count=0
        
        # declare a dataFrame object and specify columns
        df = pd.DataFrame(columns=['#', 'SerialNumber', 'Datetime', 'A_Measured_Bias','B_Measured_Bias','A_Set_Bias','B_Set_Bias','A_Diff','B_Diff','Designation'])
        
        # declare vars for lists
        Counts=[]
        SerialNumbers=[]
        A_Measured_List=[]
        B_Measured_List=[]
        A_Set_List=[]
        B_Set_List=[]
        Designations=[]
        diff_as=[]
        diff_bs=[]
        datetimes_test=[]
        
        # gather all data and put into list
        for matfile in fileslist:
            mat = scipy.io.loadmat(matfile)
            print("Running on " + str(matfile))
            DifferenceAllowed=1.8
            a_measured_bias=mat['Vbias'][0,0]
            b_measured_bias=mat['Vbias'][1,0]
            a_set_bias=mat['setBias'][0,0][0][0][0]
            b_set_bias=mat['setBias'][0,0][2][0][0]
            tmpA=abs(a_set_bias+a_measured_bias)
            tmpB=abs(b_set_bias+b_measured_bias)
            datetest = mat["rcon"][0][0][16][0]
            textString=''
            if (tmpA >= DifferenceAllowed) or (tmpB >= DifferenceAllowed):
                textString="FAIL"
            else:
                textString="PASS"
            filepathcomponents=matfile.split('\\')
            serialNumber=filepathcomponents[5]
            
            # append data to lists
            Counts.append(count)
            SerialNumbers.append(serialNumber)
            A_Measured_List.append(a_measured_bias)
            B_Measured_List.append(b_measured_bias)
            A_Set_List.append(a_set_bias)
            B_Set_List.append(b_set_bias)
            Designations.append(textString)    
            diff_as.append(tmpA)
            diff_bs.append(tmpB)
            datetimes_test.append(datetest)
            # increment counter
            count=count+1        
            
        data={'SerialNumber':SerialNumbers, 'A_Measured_Bias':A_Measured_List, 'B_Measured_Bias':B_Measured_List,
                            'A_Diff':diff_as,'B_Diff':diff_bs, 'Datetime':datetimes_test,
                            'A_Set_Bias':A_Set_List, 'B_Set_Bias':B_Set_List, 'Designation':Designations}
        df=pd.DataFrame(data)
        return df

    # create an excel file for all data found
    def create_excel_table_for_data(self,dataFrame):
        # saving the excel
        dataFrame.to_excel(self.excelSavePath)
        print('DataFrame has been written to Excel File successfully.')


ag=AggregateAllPANODEData()
ag.listnames()

