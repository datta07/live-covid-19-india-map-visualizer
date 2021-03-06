import sqlite3
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import numpy as np
import requests
from difflib import SequenceMatcher
import matplotlib



# for adding up values
def fixAltName(name,altName):
	con = sqlite3.connect('altNames.db')
	con.execute('insert into altNames values(?,?)',(name,altName))
	con.commit()
	print('added',name,'as',altName)
	con.close()

# for getting values
def getAltName(name):
	con = sqlite3.connect('altNames.db')
	data = con.execute('select altName from altNames where name=?',(name,))
	name = False
	for i in data:
		name = i[0]
	con.commit()
	con.close()
	return name


# to check all the districts are in map
def load_data(res):
	global data,infected,checkpt
	def similar(a, b):
	    return SequenceMatcher(None, a, b).ratio()
	print('checking response districts to map info\n')
	districts_map = {'Nicobar Islands': 'Andaman and Nicobar', 'North and Middle Andaman': 'Andaman and Nicobar', 'South Andaman': 'Andaman and Nicobar', 'Anantapur': 'Andhra Pradesh', 'Chittoor': 'Andhra Pradesh', 'East Godavari': 'Andhra Pradesh', 'Guntur': 'Andhra Pradesh', 'Krishna': 'Andhra Pradesh', 'Kurnool': 'Andhra Pradesh', 'Nellore': 'Andhra Pradesh', 'Prakasam': 'Andhra Pradesh', 'Srikakulam': 'Andhra Pradesh', 'Visakhapatnam': 'Andhra Pradesh', 'Vizianagaram': 'Andhra Pradesh', 'West Godavari': 'Andhra Pradesh', 'Y.S.R.': 'Andhra Pradesh', 'Anjaw': 'Arunachal Pradesh', 'Changlang': 'Arunachal Pradesh', 'Dibang Valley': 'Arunachal Pradesh', 'East Kameng': 'Arunachal Pradesh', 'East Siang': 'Arunachal Pradesh', 'Kurung Kumey': 'Arunachal Pradesh', 'Lohit': 'Arunachal Pradesh', 'Longding': 'Arunachal Pradesh', 'Lower Dibang Valley': 'Arunachal Pradesh', 'Lower Subansiri': 'Arunachal Pradesh', 'Namsai': 'Arunachal Pradesh', 'Papum Pare': 'Arunachal Pradesh', 'Tawang': 'Arunachal Pradesh', 'Tirap': 'Arunachal Pradesh', 'Upper Siang': 'Arunachal Pradesh', 'Upper Subansiri': 'Arunachal Pradesh', 'West Kameng': 'Arunachal Pradesh', 'West Siang': 'Arunachal Pradesh', 'Baksa': 'Assam', 'Barpeta': 'Assam', 'Bongaigaon': 'Assam', 'Cachar': 'Assam', 'Chirang': 'Assam', 'Darrang': 'Assam', 'Dhemaji': 'Assam', 'Dhubri': 'Assam', 'Dibrugarh': 'Assam', 'Dima Hasao': 'Assam', 'Goalpara': 'Assam', 'Golaghat': 'Assam', 'Hailakandi': 'Assam', 'Jorhat': 'Assam', 'Kamrup Metropolitan': 'Assam', 'Kamrup': 'Assam', 'Karbi Anglong': 'Assam', 'Karimganj': 'Assam', 'Kokrajhar': 'Assam', 'Lakhimpur': 'Assam', 'Morigaon': 'Assam', 'Nagaon': 'Assam', 'Nalbari': 'Assam', 'Sivasagar': 'Assam', 'Sonitpur': 'Assam', 'Tinsukia': 'Assam', 'Udalguri': 'Assam', 'Araria': 'Bihar', 'Arwal': 'Bihar', 'Aurangabad': 'Maharashtra', 'Banka': 'Bihar', 'Begusarai': 'Bihar', 'Bhagalpur': 'Bihar', 'Bhojpur': 'Bihar', 'Buxar': 'Bihar', 'Darbhanga': 'Bihar', 'Gaya': 'Bihar', 'Gopalganj': 'Bihar', 'Jamui': 'Bihar', 'Jehanabad': 'Bihar', 'Kaimur': 'Bihar', 'Katihar': 'Bihar', 'Khagaria': 'Bihar', 'Kishanganj': 'Bihar', 'Lakhisarai': 'Bihar', 'Madhepura': 'Bihar', 'Madhubani': 'Bihar', 'Munger': 'Bihar', 'Muzaffarpur': 'Bihar', 'Nalanda': 'Bihar', 'Nawada': 'Bihar', 'Pashchim Champaran': 'Bihar', 'Patna': 'Bihar', 'Purba Champaran': 'Bihar', 'Purnia': 'Bihar', 'Rohtas': 'Bihar', 'Saharsa': 'Bihar', 'Samastipur': 'Bihar', 'Saran': 'Bihar', 'Sheikhpura': 'Bihar', 'Sheohar': 'Bihar', 'Sitamarhi': 'Bihar', 'Siwan': 'Bihar', 'Supaul': 'Bihar', 'Vaishali': 'Bihar', 'Chandigarh': 'Chandigarh', 'Baloda Bazar': 'Chhattisgarh', 'Balod': 'Chhattisgarh', 'Balrampur': 'Uttar Pradesh', 'Bastar': 'Chhattisgarh', 'Bemetara': 'Chhattisgarh', 'Bijapur': 'Karnataka', 'Bilaspur': 'Himachal Pradesh', 'Dantewada': 'Chhattisgarh', 'Dhamtari': 'Chhattisgarh', 'Durg': 'Chhattisgarh', 'Gariaband': 'Chhattisgarh', 'Janjgir-Champa': 'Chhattisgarh', 'Jashpur': 'Chhattisgarh', 'Kabeerdham': 'Chhattisgarh', 'Kondagaon': 'Chhattisgarh', 'Korba': 'Chhattisgarh', 'Koriya': 'Chhattisgarh', 'Mahasamund': 'Chhattisgarh', 'Mungeli': 'Chhattisgarh', 'Narayanpur': 'Chhattisgarh', 'Raigarh': 'Maharashtra', 'Raipur': 'Chhattisgarh', 'Rajnandgaon': 'Chhattisgarh', 'Sukma': 'Chhattisgarh', 'Surajpur': 'Chhattisgarh', 'Surguja': 'Chhattisgarh', 'Uttar Bastar Kanker': 'Chhattisgarh', 'Dadra and Nagar Haveli': 'Dadra and Nagar Haveli', 'Daman': 'Daman and Diu', 'Diu': 'Daman and Diu', 'North Goa': 'Goa', 'South Goa': 'Goa', 'Ahmadabad': 'Gujarat', 'Amreli': 'Gujarat', 'Anand': 'Gujarat', 'Aravalli': 'Gujarat', 'Banas Kantha': 'Gujarat', 'Bharuch': 'Gujarat', 'Bhavnagar': 'Gujarat', 'Botad': 'Gujarat', 'Chhota Udaipur': 'Gujarat', 'Dahod': 'Gujarat', 'Devbhumi Dwarka': 'Gujarat', 'Gandhinagar': 'Gujarat', 'Gir Somnath': 'Gujarat', 'Jamnagar': 'Gujarat', 'Junagadh': 'Gujarat', 'Kachchh': 'Gujarat', 'Kheda': 'Gujarat', 'Mahesana': 'Gujarat', 'Mahisagar': 'Gujarat', 'Morbi': 'Gujarat', 'Narmada': 'Gujarat', 'Navsari': 'Gujarat', 'Panch Mahals': 'Gujarat', 'Patan': 'Gujarat', 'Porbandar': 'Gujarat', 'Rajkot': 'Gujarat', 'Sabar Kantha': 'Gujarat', 'Surat': 'Gujarat', 'Surendranagar': 'Gujarat', 'Tapi': 'Gujarat', 'The Dangs': 'Gujarat', 'Vadodara': 'Gujarat', 'Valsad': 'Gujarat', 'Ambala': 'Haryana', 'Bhiwani': 'Haryana', 'Faridabad': 'Haryana', 'Fatehabad': 'Haryana', 'Gurgaon': 'Haryana', 'Hisar': 'Haryana', 'Jhajjar': 'Haryana', 'Jind': 'Haryana', 'Kaithal': 'Haryana', 'Karnal': 'Haryana', 'Kurukshetra': 'Haryana', 'Mahendragarh': 'Haryana', 'Mewat': 'Haryana', 'Palwal': 'Haryana', 'Panchkula': 'Haryana', 'Panipat': 'Haryana', 'Rewari': 'Haryana', 'Rohtak': 'Haryana', 'Sirsa': 'Haryana', 'Sonipat': 'Haryana', 'Yamunanagar': 'Haryana', 'Chamba': 'Himachal Pradesh', 'Hamirpur': 'Uttar Pradesh', 'Kangra': 'Himachal Pradesh', 'Kinnaur': 'Himachal Pradesh', 'Kullu': 'Himachal Pradesh', 'Lahul & Spiti': 'Himachal Pradesh', 'Mandi': 'Himachal Pradesh', 'Shimla': 'Himachal Pradesh', 'Sirmaur': 'Himachal Pradesh', 'Solan': 'Himachal Pradesh', 'Una': 'Himachal Pradesh', 'Anantnag': 'Jammu and Kashmir', 'Badgam': 'Jammu and Kashmir', 'Bandipore': 'Jammu and Kashmir', 'Baramulla': 'Jammu and Kashmir', 'Doda': 'Jammu and Kashmir', 'Ganderbal': 'Jammu and Kashmir', 'Jammu': 'Jammu and Kashmir', 'Kargil': 'Jammu and Kashmir', 'Kathua': 'Jammu and Kashmir', 'Kishtwar': 'Jammu and Kashmir', 'Kulgam': 'Jammu and Kashmir', 'Kupwara': 'Jammu and Kashmir', 'Leh (Ladakh)': 'Jammu and Kashmir', 'Poonch': 'Jammu and Kashmir', 'Pulwama': 'Jammu and Kashmir', 'Rajouri': 'Jammu and Kashmir', 'Ramban': 'Jammu and Kashmir', 'Reasi': 'Jammu and Kashmir', 'Samba': 'Jammu and Kashmir', 'Shupiyan': 'Jammu and Kashmir', 'Srinagar': 'Jammu and Kashmir', 'Udhampur': 'Jammu and Kashmir', 'Bokaro': 'Jharkhand', 'Chatra': 'Jharkhand', 'Deoghar': 'Jharkhand', 'Dhanbad': 'Jharkhand', 'Dumka': 'Jharkhand', 'Garhwa': 'Jharkhand', 'Giridih': 'Jharkhand', 'Godda': 'Jharkhand', 'Gumla': 'Jharkhand', 'Hazaribagh': 'Jharkhand', 'Jamtara': 'Jharkhand', 'Khunti': 'Jharkhand', 'Kodarma': 'Jharkhand', 'Latehar': 'Jharkhand', 'Lohardaga': 'Jharkhand', 'Pakur': 'Jharkhand', 'Palamu': 'Jharkhand', 'Pashchimi Singhbhum': 'Jharkhand', 'Purbi Singhbhum': 'Jharkhand', 'Ramgarh': 'Jharkhand', 'Ranchi': 'Jharkhand', 'Sahibganj': 'Jharkhand', 'Saraikela-kharsawan': 'Jharkhand', 'Simdega': 'Jharkhand', 'Bagalkot': 'Karnataka', 'Bangalore Rural': 'Karnataka', 'Bangalore': 'Karnataka', 'Belgaum': 'Karnataka', 'Bellary': 'Karnataka', 'Bidar': 'Karnataka', 'Chamrajnagar': 'Karnataka', 'Chikballapura': 'Karnataka', 'Chikmagalur': 'Karnataka', 'Chitradurga': 'Karnataka', 'Dakshina Kannada': 'Karnataka', 'Davanagere': 'Karnataka', 'Dharwad': 'Karnataka', 'Gadag': 'Karnataka', 'Gulbarga': 'Karnataka', 'Hassan': 'Karnataka', 'Haveri': 'Karnataka', 'Kodagu': 'Karnataka', 'Kolar': 'Karnataka', 'Koppal': 'Karnataka', 'Mandya': 'Karnataka', 'Mysore': 'Karnataka', 'Raichur': 'Karnataka', 'Ramanagara': 'Karnataka', 'Shimoga': 'Karnataka', 'Tumkur': 'Karnataka', 'Udupi': 'Karnataka', 'Uttara Kannada': 'Karnataka', 'Yadgir': 'Karnataka', 'Alappuzha': 'Kerala', 'Ernakulam': 'Kerala', 'Idukki': 'Kerala', 'Kannur': 'Kerala', 'Kasaragod': 'Kerala', 'Kollam': 'Kerala', 'Kottayam': 'Kerala', 'Kozhikode': 'Kerala', 'Malappuram': 'Kerala', 'Palakkad': 'Kerala', 'Pathanamthitta': 'Kerala', 'Thiruvananthapuram': 'Kerala', 'Thrissur': 'Kerala', 'Wayanad': 'Kerala', 'Lakshadweep': 'Lakshadweep', 'Agar Malwa': 'Madhya Pradesh', 'Alirajpur': 'Madhya Pradesh', 'Anuppur': 'Madhya Pradesh', 'Ashoknagar': 'Madhya Pradesh', 'Balaghat': 'Madhya Pradesh', 'Barwani': 'Madhya Pradesh', 'Betul': 'Madhya Pradesh', 'Bhind': 'Madhya Pradesh', 'Bhopal': 'Madhya Pradesh', 'Burhanpur': 'Madhya Pradesh', 'Chhatarpur': 'Madhya Pradesh', 'Chhindwara': 'Madhya Pradesh', 'Damoh': 'Madhya Pradesh', 'Datia': 'Madhya Pradesh', 'Dewas': 'Madhya Pradesh', 'Dhar': 'Madhya Pradesh', 'Dindori': 'Madhya Pradesh', 'East Nimar': 'Madhya Pradesh', 'Guna': 'Madhya Pradesh', 'Gwalior': 'Madhya Pradesh', 'Harda': 'Madhya Pradesh', 'Hoshangabad': 'Madhya Pradesh', 'Indore': 'Madhya Pradesh', 'Jabalpur': 'Madhya Pradesh', 'Jhabua': 'Madhya Pradesh', 'Katni': 'Madhya Pradesh', 'Mandla': 'Madhya Pradesh', 'Mandsaur': 'Madhya Pradesh', 'Morena': 'Madhya Pradesh', 'Narsimhapur': 'Madhya Pradesh', 'Neemuch': 'Madhya Pradesh', 'Panna': 'Madhya Pradesh', 'Raisen': 'Madhya Pradesh', 'Rajgarh': 'Madhya Pradesh', 'Ratlam': 'Madhya Pradesh', 'Rewa': 'Madhya Pradesh', 'Sagar': 'Madhya Pradesh', 'Satna': 'Madhya Pradesh', 'Sehore': 'Madhya Pradesh', 'Seoni': 'Madhya Pradesh', 'Shahdol': 'Madhya Pradesh', 'Shajapur': 'Madhya Pradesh', 'Sheopur': 'Madhya Pradesh', 'Shivpuri': 'Madhya Pradesh', 'Sidhi': 'Madhya Pradesh', 'Singrauli': 'Madhya Pradesh', 'Tikamgarh': 'Madhya Pradesh', 'Ujjain': 'Madhya Pradesh', 'Umaria': 'Madhya Pradesh', 'Vidisha': 'Madhya Pradesh', 'West Nimar': 'Madhya Pradesh', 'Ahmadnagar': 'Maharashtra', 'Akola': 'Maharashtra', 'Amravati': 'Maharashtra', 'Bhandara': 'Maharashtra', 'Bid': 'Maharashtra', 'Buldana': 'Maharashtra', 'Chandrapur': 'Maharashtra', 'Dhule': 'Maharashtra', 'Garhchiroli': 'Maharashtra', 'Gondiya': 'Maharashtra', 'Hingoli': 'Maharashtra', 'Jalgaon': 'Maharashtra', 'Jalna': 'Maharashtra', 'Kolhapur': 'Maharashtra', 'Latur': 'Maharashtra', 'Mumbai City': 'Maharashtra', 'Mumbai Suburban': 'Maharashtra', 'Nagpur': 'Maharashtra', 'Nanded': 'Maharashtra', 'Nandurbar': 'Maharashtra', 'Nashik': 'Maharashtra', 'Osmanabad': 'Maharashtra', 'Palghar': 'Maharashtra', 'Parbhani': 'Maharashtra', 'Pune': 'Maharashtra', 'Ratnagiri': 'Maharashtra', 'Sangli': 'Maharashtra', 'Satara': 'Maharashtra', 'Sindhudurg': 'Maharashtra', 'Solapur': 'Maharashtra', 'Thane': 'Maharashtra', 'Wardha': 'Maharashtra', 'Washim': 'Maharashtra', 'Yavatmal': 'Maharashtra', 'Bishnupur': 'Manipur', 'Chandel': 'Manipur', 'Churachandpur': 'Manipur', 'Imphal East': 'Manipur', 'Imphal West': 'Manipur', 'Senapati': 'Manipur', 'Tamenglong': 'Manipur', 'Thoubal': 'Manipur', 'Ukhrul': 'Manipur', 'East Garo Hills': 'Meghalaya', 'East Khasi Hills': 'Meghalaya', 'Jaintia Hills': 'Meghalaya', 'North Garo Hills': 'Meghalaya', 'Ri Bhoi': 'Meghalaya', 'South Garo Hills': 'Meghalaya', 'South West Garo Hills': 'Meghalaya', 'South West Khasi Hills': 'Meghalaya', 'West Garo Hills': 'Meghalaya', 'West Khasi Hills': 'Meghalaya', 'Aizawl': 'Mizoram', 'Champhai': 'Mizoram', 'Kolasib': 'Mizoram', 'Lawangtlai': 'Mizoram', 'Lunglei': 'Mizoram', 'Mamit': 'Mizoram', 'Saiha': 'Mizoram', 'Serchhip': 'Mizoram', 'Dimapur': 'Nagaland', 'Kiphire': 'Nagaland', 'Kohima': 'Nagaland', 'Longleng': 'Nagaland', 'Mokokchung': 'Nagaland', 'Mon': 'Nagaland', 'Peren': 'Nagaland', 'Phek': 'Nagaland', 'Tuensang': 'Nagaland', 'Wokha': 'Nagaland', 'Zunheboto': 'Nagaland', 'West': 'NCT of Delhi', 'Anugul': 'Odisha', 'Balangir': 'Odisha', 'Baleshwar': 'Odisha', 'Bargarh': 'Odisha', 'Bauda': 'Odisha', 'Bhadrak': 'Odisha', 'Cuttack': 'Odisha', 'Debagarh': 'Odisha', 'Dhenkanal': 'Odisha', 'Gajapati': 'Odisha', 'Ganjam': 'Odisha', 'Jagatsinghapur': 'Odisha', 'Jajapur': 'Odisha', 'Jharsuguda': 'Odisha', 'Kalahandi': 'Odisha', 'Kandhamal': 'Odisha', 'Kendrapara': 'Odisha', 'Kendujhar': 'Odisha', 'Khordha': 'Odisha', 'Koraput': 'Odisha', 'Malkangiri': 'Odisha', 'Mayurbhanj': 'Odisha', 'Nabarangapur': 'Odisha', 'Nayagarh': 'Odisha', 'Nuapada': 'Odisha', 'Puri': 'Odisha', 'Rayagada': 'Odisha', 'Sambalpur': 'Odisha', 'Subarnapur': 'Odisha', 'Sundargarh': 'Odisha', 'Karaikal': 'Puducherry', 'Mahe': 'Puducherry', 'Puducherry': 'Puducherry', 'Yanam': 'Puducherry', 'Amritsar': 'Punjab', 'Barnala': 'Punjab', 'Bathinda': 'Punjab', 'Faridkot': 'Punjab', 'Fatehgarh Sahib': 'Punjab', 'Fazilka': 'Punjab', 'Firozpur': 'Punjab', 'Gurdaspur': 'Punjab', 'Hoshiarpur': 'Punjab', 'Jalandhar': 'Punjab', 'Kapurthala': 'Punjab', 'Ludhiana': 'Punjab', 'Mansa': 'Punjab', 'Moga': 'Punjab', 'Muktsar': 'Punjab', 'Pathankot': 'Punjab', 'Patiala': 'Punjab', 'Rupnagar': 'Punjab', 'Sahibzada Ajit Singh Nagar': 'Punjab', 'Sangrur': 'Punjab', 'Shahid Bhagat Singh Nagar': 'Punjab', 'Tarn Taran': 'Punjab', 'Ajmer': 'Rajasthan', 'Alwar': 'Rajasthan', 'Banswara': 'Rajasthan', 'Baran': 'Rajasthan', 'Barmer': 'Rajasthan', 'Bharatpur': 'Rajasthan', 'Bhilwara': 'Rajasthan', 'Bikaner': 'Rajasthan', 'Bundi': 'Rajasthan', 'Chittaurgarh': 'Rajasthan', 'Churu': 'Rajasthan', 'Dausa': 'Rajasthan', 'Dhaulpur': 'Rajasthan', 'Dungarpur': 'Rajasthan', 'Ganganagar': 'Rajasthan', 'Hanumangarh': 'Rajasthan', 'Jaipur': 'Rajasthan', 'Jaisalmer': 'Rajasthan', 'Jalor': 'Rajasthan', 'Jhalawar': 'Rajasthan', 'Jhunjhunun': 'Rajasthan', 'Jodhpur': 'Rajasthan', 'Karauli': 'Rajasthan', 'Kota': 'Rajasthan', 'Nagaur': 'Rajasthan', 'Pali': 'Rajasthan', 'Pratapgarh': 'Uttar Pradesh', 'Rajsamand': 'Rajasthan', 'Sawai Madhopur': 'Rajasthan', 'Sikar': 'Rajasthan', 'Sirohi': 'Rajasthan', 'Tonk': 'Rajasthan', 'Udaipur': 'Rajasthan', 'East Sikkim': 'Sikkim', 'North Sikkim': 'Sikkim', 'South Sikkim': 'Sikkim', 'West Sikkim': 'Sikkim', 'Ariyalur': 'Tamil Nadu', 'Chennai': 'Tamil Nadu', 'Coimbatore': 'Tamil Nadu', 'Cuddalore': 'Tamil Nadu', 'Dharmapuri': 'Tamil Nadu', 'Dindigul': 'Tamil Nadu', 'Erode': 'Tamil Nadu', 'Kancheepuram': 'Tamil Nadu', 'Kanniyakumari': 'Tamil Nadu', 'Karur': 'Tamil Nadu', 'Krishnagiri': 'Tamil Nadu', 'Madurai': 'Tamil Nadu', 'Nagappattinam': 'Tamil Nadu', 'Namakkal': 'Tamil Nadu', 'Perambalur': 'Tamil Nadu', 'Pudukkottai': 'Tamil Nadu', 'Ramanathapuram': 'Tamil Nadu', 'Salem': 'Tamil Nadu', 'Sivaganga': 'Tamil Nadu', 'Thanjavur': 'Tamil Nadu', 'The Nilgiris': 'Tamil Nadu', 'Theni': 'Tamil Nadu', 'Thiruvallur': 'Tamil Nadu', 'Thiruvarur': 'Tamil Nadu', 'Thoothukkudi': 'Tamil Nadu', 'Tiruchirappalli': 'Tamil Nadu', 'Tirunelveli': 'Tamil Nadu', 'Tiruppur': 'Tamil Nadu', 'Tiruvannamalai': 'Tamil Nadu', 'Vellore': 'Tamil Nadu', 'Viluppuram': 'Tamil Nadu', 'Virudunagar': 'Tamil Nadu', 'Adilabad': 'Telangana', 'Hyderabad': 'Telangana', 'Karimnagar': 'Telangana', 'Khammam': 'Telangana', 'Mahbubnagar': 'Telangana', 'Medak': 'Telangana', 'Nalgonda': 'Telangana', 'Nizamabad': 'Telangana', 'Ranga Reddy': 'Telangana', 'Warangal': 'Telangana', 'Dhalai': 'Tripura', 'Gomati': 'Tripura', 'Khowai': 'Tripura', 'North Tripura': 'Tripura', 'Sipahijala': 'Tripura', 'South Tripura': 'Tripura', 'Unokoti': 'Tripura', 'West Tripura': 'Tripura', 'Agra': 'Uttar Pradesh', 'Aligarh': 'Uttar Pradesh', 'Allahabad': 'Uttar Pradesh', 'Ambedkar Nagar': 'Uttar Pradesh', 'Amethi': 'Uttar Pradesh', 'Amroha': 'Uttar Pradesh', 'Auraiya': 'Uttar Pradesh', 'Azamgarh': 'Uttar Pradesh', 'Baghpat': 'Uttar Pradesh', 'Bahraich': 'Uttar Pradesh', 'Ballia': 'Uttar Pradesh', 'Banda': 'Uttar Pradesh', 'Barabanki': 'Uttar Pradesh', 'Bareilly': 'Uttar Pradesh', 'Basti': 'Uttar Pradesh', 'Bijnor': 'Uttar Pradesh', 'Budaun': 'Uttar Pradesh', 'Bulandshahr': 'Uttar Pradesh', 'Chandauli': 'Uttar Pradesh', 'Chitrakoot': 'Uttar Pradesh', 'Deoria': 'Uttar Pradesh', 'Etah': 'Uttar Pradesh', 'Etawah': 'Uttar Pradesh', 'Faizabad': 'Uttar Pradesh', 'Farrukhabad': 'Uttar Pradesh', 'Fatehpur': 'Uttar Pradesh', 'Firozabad': 'Uttar Pradesh', 'Gautam Buddha Nagar': 'Uttar Pradesh', 'Ghaziabad': 'Uttar Pradesh', 'Ghazipur': 'Uttar Pradesh', 'Gonda': 'Uttar Pradesh', 'Gorakhpur': 'Uttar Pradesh', 'Hapur': 'Uttar Pradesh', 'Hardoi': 'Uttar Pradesh', 'Hathras': 'Uttar Pradesh', 'Jalaun': 'Uttar Pradesh', 'Jaunpur': 'Uttar Pradesh', 'Jhansi': 'Uttar Pradesh', 'Kannauj': 'Uttar Pradesh', 'Kanpur Dehat': 'Uttar Pradesh', 'Kanpur Nagar': 'Uttar Pradesh', 'Kasganj': 'Uttar Pradesh', 'Kaushambi': 'Uttar Pradesh', 'Kushinagar': 'Uttar Pradesh', 'Lakhimpur Kheri': 'Uttar Pradesh', 'Lalitpur': 'Uttar Pradesh', 'Lucknow': 'Uttar Pradesh', 'Maharajganj': 'Uttar Pradesh', 'Mahoba': 'Uttar Pradesh', 'Mainpuri': 'Uttar Pradesh', 'Mathura': 'Uttar Pradesh', 'Mau': 'Uttar Pradesh', 'Meerut': 'Uttar Pradesh', 'Mirzapur': 'Uttar Pradesh', 'Moradabad': 'Uttar Pradesh', 'Muzaffarnagar': 'Uttar Pradesh', 'Pilibhit': 'Uttar Pradesh', 'Rae Bareli': 'Uttar Pradesh', 'Rampur': 'Uttar Pradesh', 'Saharanpur': 'Uttar Pradesh', 'Sambhal': 'Uttar Pradesh', 'Sant Kabir Nagar': 'Uttar Pradesh', 'Sant Ravi Das Nagar': 'Uttar Pradesh', 'Shahjahanpur': 'Uttar Pradesh', 'Shamli': 'Uttar Pradesh', 'Shravasti': 'Uttar Pradesh', 'Siddharth Nagar': 'Uttar Pradesh', 'Sitapur': 'Uttar Pradesh', 'Sonbhadra': 'Uttar Pradesh', 'Sultanpur': 'Uttar Pradesh', 'Unnao': 'Uttar Pradesh', 'Varanasi': 'Uttar Pradesh', 'Almora': 'Uttarakhand', 'Bageshwar': 'Uttarakhand', 'Chamoli': 'Uttarakhand', 'Champawat': 'Uttarakhand', 'Dehradun': 'Uttarakhand', 'Garhwal': 'Uttarakhand', 'Hardwar': 'Uttarakhand', 'Nainital': 'Uttarakhand', 'Pithoragarh': 'Uttarakhand', 'Rudraprayag': 'Uttarakhand', 'Tehri Garhwal': 'Uttarakhand', 'Udham Singh Nagar': 'Uttarakhand', 'Uttarkashi': 'Uttarakhand', 'Alipurduar': 'West Bengal', 'Bankura': 'West Bengal', 'Barddhaman': 'West Bengal', 'Birbhum': 'West Bengal', 'Dakshin Dinajpur': 'West Bengal', 'Darjiling': 'West Bengal', 'Haora': 'West Bengal', 'Hugli': 'West Bengal', 'Jalpaiguri': 'West Bengal', 'Koch Bihar': 'West Bengal', 'Kolkata': 'West Bengal', 'Maldah': 'West Bengal', 'Murshidabad': 'West Bengal', 'Nadia': 'West Bengal', 'North 24 Parganas': 'West Bengal', 'Pashchim Medinipur': 'West Bengal', 'Purba Medinipur': 'West Bengal', 'Puruliya': 'West Bengal', 'South 24 Parganas': 'West Bengal', 'Uttar Dinajpur': 'West Bengal'}
	for i in res:
		altName=getAltName(i)
		if (altName):
			if (altName in districts_map):
				data[altName]=res[i]
				infected.append(res[i]['infected'])
			else:
				print(i,altName,'not found in map info')
		else:
			if i in districts_map:
				print('updating',i,'as found in data\n')
				fixAltName(i,i)
			else:
				sim={}
				for j in districts_map:
					sim[j]=similar(i,j)
				print('ignoring ',i)
				print('        -> may be-',max(sim, key=sim.get),sim[max(sim, key=sim.get)])
	print('## Update the unsaved districts in database (use districts.txt)')

	## clustering data for colors
	# divide data to 10 parts
	infected.sort()
	print(infected)
	n=len(infected)//10
	checkpt=[]
	for i in range(10):
		checkpt.append(infected[(i)*n])
	print('fixing check points as ',checkpt)

# Adding colors
def colorPicker(val):
	# cluster the data into 10 parts based on frequency
	global checkpt
	cmap = matplotlib.cm.get_cmap('Reds')
	values=[0.2,0.3,0.4,0.5,0.6,0.65,0.7,0.8,0.9]
	for no in range(9):
		if (checkpt[no]>=val):
			return matplotlib.colors.to_hex(cmap(values[no]), keep_alpha=True)
	return matplotlib.colors.to_hex(cmap(0.999), keep_alpha=True)



data={}
infected=[]
checkpt=[]
res = requests.get('https://v1.api.covindia.com/district-values').json()
load_data(res) #check data


# plotting map
print('\n  ploting map  , Loading...')
fig, ax = plt.subplots()
map=Basemap(projection="mill",lat_0=54.5, lon_0=-4.36,llcrnrlon=67.8, llcrnrlat=5.5, urcrnrlon=97.4, urcrnrlat=37.5)
map.readshapefile('data/IND_adm2','INDIA')

patchs=[]
#data sample -> {'dead': 0, 'infected': 1, 'state': 'Gujarat', 'value': 0.006369426751592357}
for info,shape in zip(map.INDIA_info, map.INDIA):
	if (info['NAME_2'] in data):
		#patchs.append(Polygon(np.array(shape), True))
		ax.add_collection(PatchCollection([Polygon(np.array(shape))], facecolor= colorPicker(data[info['NAME_2']]['infected']), edgecolor='k', linewidths=.3, zorder=2))
		#ax.add_collection(PatchCollection([Polygon(np.array(shape))], facecolor= '#ffffff' , edgecolor='k', linewidths=.2, zorder=2))
	else:
		ax.add_collection(PatchCollection([Polygon(np.array(shape))], facecolor= '#ffffff' , edgecolor='k', linewidths=.2, zorder=2))
		#ax.add_collection(PatchCollection([Polygon(np.array(shape))], facecolor= (0,1,0,1) , edgecolor='k', linewidths=.2, zorder=2))


plt.title('Corona Effected Districts')
plt.show()
