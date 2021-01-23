import pandas as pd
import io
import requests
url="http://www.chp.gov.hk/files/misc/enhanced_sur_covid_19_eng.csv"
s=requests.get(url).content
df=pd.read_csv(io.StringIO(s.decode('utf-8')))


################ Part 1 : Normal actual case



#Create the table for case classification 
#   Row - report date
#   Column - 4 - llp,lln,ip,in


#df=df[1113:4692]

# Local link (+) ,Local link (-), Imported link (+) and Imported link (-) dataframes
df_lln = df[df["Case classification*"]== "Local case"]
df_llp = df[df["Case classification*"]== "Epidemiologically linked with local case"]
df_ilp = df[df["Case classification*"]== "Epidemiologically linked with imported case"]
df_iln = df[df["Case classification*"]== "Imported case"]

# Make the Reported date as datetime type
s = pd.to_datetime(df_lln["Report date"],format='%d/%m/%Y').dt.date
df_lln = df_lln.assign(e=pd.Series(s).values)
df_lln = df_lln.drop(["Report date"], axis=1)
df_lln.rename(columns={'e': 'Report date'}, inplace=True)

s = pd.to_datetime(df_llp["Report date"],format='%d/%m/%Y').dt.date
df_llp = df_llp.assign(e=pd.Series(s).values)
df_llp = df_llp.drop(["Report date"], axis=1)
df_llp.rename(columns={'e': 'Report date'}, inplace=True)

s = pd.to_datetime(df_iln["Report date"],format='%d/%m/%Y').dt.date
df_iln = df_iln.assign(e=pd.Series(s).values)
df_iln = df_iln.drop(["Report date"], axis=1)
df_iln.rename(columns={'e': 'Report date'}, inplace=True)

s = pd.to_datetime(df_ilp["Report date"],format='%d/%m/%Y').dt.date
df_ilp = df_ilp.assign(e=pd.Series(s).values)
df_ilp = df_ilp.drop(["Report date"], axis=1)
df_ilp.rename(columns={'e': 'Report date'}, inplace=True)

#Group by report date 
df_llp=df_llp.groupby("Report date").count()
df_lln=df_lln.groupby("Report date").count()
df_iln=df_iln.groupby("Report date").count()
df_ilp=df_ilp.groupby("Report date").count()

#Drop the columns except case number 
df_llp=df_llp.drop(df.columns[2:],axis=1)
df_lln=df_lln.drop(df.columns[2:],axis=1)
df_ilp=df_ilp.drop(df.columns[2:],axis=1)
df_iln=df_iln.drop(df.columns[2:],axis=1)

#Rename columns 
df_lln =df_lln.rename(columns={"Case no.": "Local link (-)"})
df_llp =df_llp.rename(columns={"Case no.": "Local link (+)"})
df_iln =df_iln.rename(columns={"Case no.": "Imported link (-)"})
df_ilp =df_ilp.rename(columns={"Case no.": "Imported link (+)"})

#Merge the dataframes into 1
df_merged=df_llp.join(df_lln,how="outer")
df_merged = df_merged.join(df_ilp,how="outer")
df_merged=df_merged.join(df_iln,how="outer")

#Replace NaN with 0
df_merged = df_merged.fillna(0)

#Add the column for total cases
df_merged["Total"]=df_merged.sum(axis=1)


################# Part 2: Now calculate the delay separately for local link + and local link - cases
df_delay_prep = df[~df['Date of onset'].isin(['Asymptomatic','Pending',"Unknown","January","Mid-March","Mid- July","Mid-July","October"])]

#Convert date of onset and reported date to datetime format
s = pd.to_datetime(df_delay_prep["Report date"],format='%d/%m/%Y').dt.date
df_delay_prep = df_delay_prep.assign(e=pd.Series(s).values)
df_delay_prep = df_delay_prep.drop(["Report date"], axis=1)
df_delay_prep.rename(columns={'e': 'Report date'}, inplace=True)

s = pd.to_datetime(df_delay_prep["Date of onset"],format='%d/%m/%Y').dt.date
df_delay_prep = df_delay_prep.assign(e=pd.Series(s).values)
df_delay_prep = df_delay_prep.drop(["Date of onset"], axis=1)
df_delay_prep.rename(columns={'e': 'Date of onset'}, inplace=True)

# Local link (+) ,Local link (-) dataframes
df_lln_v5 = df_delay_prep[df_delay_prep["Case classification*"]== "Local case"]
df_llp_v5 = df_delay_prep[df_delay_prep["Case classification*"]== "Epidemiologically linked with local case"]

#Calculate delay
df_lln_v5["Delay"]=df_lln_v5["Report date"].sub(df_lln_v5["Date of onset"],axis=0)
df_llp_v5["Delay"]=df_llp_v5["Report date"].sub(df_llp_v5["Date of onset"],axis=0)

#Convert delay to int
df_lln_v5["Delay"]=df_lln_v5["Delay"].dt.days
df_llp_v5["Delay"]=df_llp_v5["Delay"].dt.days

#Rename columns
df_llp_v5 = df_llp_v5.rename(columns={"Delay":"Delay local link (+)"})
df_lln_v5 = df_lln_v5.rename(columns={"Delay":"Delay local link (-)"})


#Groupby report date
df_for_sw_3 = df_lln_v5.groupby(["Report date"]).sum()  # sw 3 - lln
df_for_sw_4 = df_llp_v5.groupby(["Report date"]).sum()  # sw 4 - llp



#Drop unrequired columns
df_for_sw_3 = df_for_sw_3.drop(columns={"Case no.","Name of hospital admitted","Age"})
df_for_sw_4 = df_for_sw_4.drop(columns={"Case no.","Name of hospital admitted","Age"})

# Note that df_for_sw_delay is the main df_for_delay

# Ensure they are of same size 
if len(df_for_sw_3)!=len(df_for_sw_4):
    df_for_sw_delay=df_for_sw_3.join(df_for_sw_4,how="outer")
    
#Make NaN = 0
df_for_sw_delay = df_for_sw_delay.fillna(0)

#Now calculate the cases with delay 
df_for_sw_5 = df_lln_v5.groupby(["Report date"]).count()#lln
df_for_sw_6 = df_llp_v5.groupby(["Report date"]).count() # llp


#Rename Case no. to Cases with delay
df_for_sw_5 =df_for_sw_5.rename(columns={"Case no.": "Cases with delay - local link (-)"})
df_for_sw_6 =df_for_sw_6.rename(columns={"Case no.": "Cases with delay - local link (+)"})

#Drop all but case no.
df_for_sw_5 = df_for_sw_5.drop(df.columns[2:],axis=1)
df_for_sw_6 = df_for_sw_6.drop(df.columns[2:],axis=1)
df_for_sw_5 = df_for_sw_5.drop(columns=["Delay local link (-)"])
df_for_sw_6 = df_for_sw_6.drop(columns=["Delay local link (+)"])

#Merge them with df_for_sw_delay
df_for_sw_delay=df_for_sw_delay.join(df_for_sw_5,how="outer")
df_for_sw_delay=df_for_sw_delay.join(df_for_sw_6,how="outer")

#Make NaN = 0
df_for_sw_delay = df_for_sw_delay.fillna(0)

################## Part 3: Now do the sliding window for delay

#Create a copy of the df_for_sw_2_modified to do the sliding window operation
sw_delay = df_for_sw_delay.copy()

#N rows
n_rows =len(df_for_sw_delay) 

#For 08 July to 21 August

i = 3 

while i < (n_rows - 3):
    sw_delay.iloc[i]= df_for_sw_delay.iloc[i-3:i+4].sum(axis=0)
    i+=1
    
# For 22 Aug to Aug 24
x = n_rows -3
i = 0
while x < (n_rows):
    sw_delay.iloc[x] = df_for_sw_delay.iloc[x-3:(x+3-i)].sum(axis=0)
    x=x+1
    i=i+1
    
# For 05 Jul to 07 July
x = 0
i = 0

while (x < 3):
    sw_delay.iloc[x]=df_for_sw_delay.iloc[(x-i):x+4].sum(axis=0)
    x=x+1
    i=i+1 

# Calculate the average delay
sw_delay["Local link (+)"]=sw_delay["Delay local link (+)"]/sw_delay["Cases with delay - local link (+)"]
sw_delay["Local link (-)"]=sw_delay["Delay local link (-)"]/sw_delay["Cases with delay - local link (-)"]

#Get today's info
last_value = len(df_merged)
today_info = df_merged[last_value-1:]

#Calculate the number of deaths 
df_dead = df.groupby(["Hospitalised/Discharged/Deceased"]).count()
n_deaths = df_dead.at["Deceased","Case no."]

#Calculate the number of confirmed cases
total_confirmed = len(df)

#Calculate the latest daily total cases 
total_today =  today_info.iloc[0,-1]

#Caculate the number of possibly local and Epidemiologically linked with possibly local case
possibly_cases = len(df[(df["Case classification*"]=="Local case") | (df["Case classification*"]=="Local case") ].index)

#More to do with today_info
s = pd.DataFrame(
    {
        "Local link (+)":"Local link (+)",
        "Local link (-)":"Local link (-)",
        "Imported link (+)":"Imported link (+)",
        "Imported link (-)":"Imported link (-)",
    },
    index=[2],
)


new_df = pd.concat([today_info,s])
new_df = new_df.T
new_df = new_df.to_numpy()
latest_info = pd.DataFrame({"Case_type":new_df[:,1],"Cases":new_df[:,0]})
last_updated = df.iloc[total_confirmed-1,1]
 

############# Part 4 : Sliding window of total cases
#Calculate the no.of rows
n_rows = df_merged.shape[0]

df_merged_copy = df_merged.copy()
#For 08 July to 21 August

i = 3 

while i < (n_rows - 3):
    df_merged_copy.iloc[i]= df_merged.iloc[i-3:i+4].sum(axis=0)
    i+=1
    
# For 22 Aug to Aug 24
x = n_rows -3
i = 0
while x < (n_rows):
    df_merged_copy.iloc[x] = df_merged.iloc[x-3:(x+3-i)].sum(axis=0)
    x=x+1
    i=i+1
    
# For 05 Jul to 07 July
x = 0
i = 0

while (x < 3):
    df_merged_copy.iloc[x]=df_merged.iloc[(x-i):x+4].sum(axis=0)
    x=x+1
    i=i+1    


###############Part 6 : Situation Reports
url="http://www.chp.gov.hk/files/misc/latest_situation_of_reported_cases_covid_19_eng.csv"
s=requests.get(url).content
df_situation=pd.read_csv(io.StringIO(s.decode('utf-8')))
df_situation = df_situation.fillna(0)
confirmed_deaths_today = df_situation.iloc[-1]["Number of death cases"] - df_situation.iloc[-2]["Number of death cases"]
discharged_cases = df_situation.iloc[-1]["Number of discharge cases"]


############## PART 7 : Mode of testing
url="http://www.chp.gov.hk/files/misc/mode_of_detection_eng.csv"
s=requests.get(url).content
df_testing=pd.read_csv(io.StringIO(s.decode('utf-8')))

################ Part 8: World Cases
df_world = pd.read_html('https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data')[0] #from wikipedia
df_world = df_world.columns.to_frame().T.append(df_world, ignore_index=True)
df_world.columns = range(len(df_world.columns))
df_world.columns = df_world.iloc[0]
df_world = df_world.iloc[1:240,1:5]

# Case details
df_details = df.drop(columns={"Confirmed/probable","Date of onset","Name of hospital admitted"},axis=1)
df_details = df_details.rename(columns={'Hospitalised/Discharged/Deceased' : 'Hospitalised /Discharged/ Deceased'})
