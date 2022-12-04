import sqlite3
import random

DB_PATH = 'PCParts_db.db' #Name of the database is set here

db = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
db.row_factory = sqlite3.Row #creates a dictionary cursor


def create_user_table():

    try:
        cursor = db.cursor()

        cursor.execute("DROP TABLE IF EXISTS User") #If user table exists, delete it and create a new one

        sql = '''CREATE TABLE IF NOT EXISTS User (
                    username VARCHAR(50) UNIQUE PRIMARY KEY,
                    password VARCHAR(100) NOT NULL)
            '''
        #SQL code that to create the User table

        cursor.execute(sql)

        db.commit()
        print("User table initialised")

    except sqlite3.Error as e:
        db.rollback()
        print(f"Unable to create User table. Error: {e}")
        raise e


def create_cpu_table():

    try:
        cursor = db.cursor()

        cursor.execute("DROP TABLE IF EXISTS CPU")

        sql = '''CREATE TABLE IF NOT EXISTS CPU (
                       CPUcode VARCHAR(10) UNIQUE PRIMARY KEY,
                       CPUName VARCHAR(100) NOT NULL,
                       Manufacturer VARCHAR(100) NOT NULL,
                       Price DECIMAL(6,2),
                       Cores INTEGER,
                       Threads INTEGER,
                       Socket VARCHAR(10),
                       ClockSpeed DECIMAL(3,2))
               '''

        cursor.execute(sql)
        cursor.execute("INSERT INTO CPU (CPUCode, CPUName, Manufacturer, Price, Cores, Threads, Socket, ClockSpeed) "
                       "VALUES "
                       "( 'Ryzen-2','Ryzen 5 3600','AMD',282.99,6,12,'AM4',3.6),"
                       "( 'Ryzen-3','Ryzen 5 5600X','AMD',265,6,12,'AM4',3.7),"
                       "( 'Ryzen-4','Ryzen 5 5600G','AMD',199.99,6,12,'AM4',3.9),"
                       "( 'Ryzen-5','Ryzen 7 5800X','AMD',327.99,8,16,'AM4',3.8),"
                       "( 'Ryzen-6','Ryzen 7 5700G','AMD',260.69,8,16,'AM4',3.8),"
                       "( 'Ryzen-7','Ryzen 7 3700X','AMD',269,8,16,'AM4',3.6),"
                       "( 'Ryzen-8','Ryzen Threadripper 1900X','AMD',161.44,8,16,'sTR4',3.8),"
                       "( 'Ryzen-9','Ryzen 5 1600','AMD',195,6,12,'AM4',3.2),"
                       "( 'Core-10','Core i5-11600K','Intel',226,6,12,'FCLGA1200',3.9),"
                       "( 'Core-11','Core i5-11400F','Intel',186.48,6,12,'FCLGA1200',2.6),"
                       "( 'Core-12','Core i3-10105F','Intel',79.96,4,8,'FCLGA1200',3.7),"
                       "( 'Core-13','Core i5-10400F','Intel',125,6,12,'FCLGA1200',2.9),"
                       "( 'Ryzen-14','Ryzen 9 5900X','AMD',449.99,12,24,'AM4',3.7),"
                       "( 'Core-15','Core i9-12900K','Intel',608.69,16,24,'FCLGA1700',3.2),"
                       "( 'Ryzen-16','Ryzen 9 5950X','AMD',657,16,32,'AM4',3.4),")

        #Inputting all the data for my CPUs here
        db.commit()
        print("CPU table initialised")

    except sqlite3.Error as e:
        db.rollback()
        print(f"Unable to create CPU table. Error: {e}")
        raise e


def create_gpu_table():

    try:
        cursor = db.cursor()

        cursor.execute("DROP TABLE IF EXISTS GPU")

        sql = '''CREATE TABLE IF NOT EXISTS GPU (
                       GPUcode VARCHAR(10) UNIQUE PRIMARY KEY,
                       GPUName VARCHAR(100) NOT NULL,
                       Manufacturer VARCHAR(100) NOT NULL,
                       Price DECIMAL(6,2),
                       Cores INTEGER,
                       VRAM Integer NOT NULL)
               '''

        cursor.execute(sql)
        cursor.execute("INSERT INTO GPU (GPUCode, GPUName, Manufacturer, Price, Cores, VRAM) "
                       "VALUES "
                       "( 'Nvidia-2','GeForce RTX 3060','Nvidia',649,3584,12),"
                       "( 'Nvidia-3','GeForce RTX 3090','Nvidia',2500,10496,24),"
                       "( 'Nvidia-4','GeForce GTX 1050 Ti','Nvidia',209.99,768,4),"
                       "( 'Nvidia-5','GeForce RTX 3060 Ti','Nvidia',699.99,4864,8),"
                       "( 'Nvidia-6','GeForce GTX 1650','Nvidia',416.91,896,4),"
                       "( 'Nvidia-7','GeForce RTX 3080','Nvidia',824.25,8704,10),"
                       "( 'Nvidia-8','GeForce GTX 960','Nvidia',284.1,1024,2),"
                       "( 'Nvidia-9','GeForce GTX 1060 6 GB','Nvidia',394.99,1280,6),"
                       "( 'Nvidia-10','GeForce RTX 3070','Nvidia',649.99,5888,8),"
                       "( 'Nvidia-11','GeForce GTX 970','Nvidia',230,1664,4),"
                       "( 'Nvidia-12','GeForce RTX 2060','Nvidia',599.99,1920,6),"
                       "( 'AMD-13','Radeon RX 6600 XT','AMD',468.99,2048,8),"
                       "( 'Nvidia-14','GeForce RTX 3080 Ti','Nvidia',1940.99,10240,12),"
                       "( 'AMD-15','Radeon RX 580','AMD',699.99,2304,8);")
        #Inputting all GPUs here
        db.commit()
        print("GPU table initialised")

    except sqlite3.Error as e:
        db.rollback()
        print(f"Unable to create GPU table. Error: {e}")
        raise e


def create_hdd_table():

    try:
        cursor = db.cursor()

        cursor.execute("DROP TABLE IF EXISTS HDD")

        sql = '''CREATE TABLE IF NOT EXISTS HDD (
                       HDDcode VARCHAR(10) UNIQUE PRIMARY KEY,
                       HDDName VARCHAR(100) NOT NULL,
                       Manufacturer VARCHAR(100) NOT NULL,
                       Price DECIMAL(6,2),
                       Capacity INTEGER,
                       ReadSpeed INTEGER,
                       WriteSpeed INTEGER)
               '''

        cursor.execute(sql)
        cursor.execute("INSERT INTO HDD (HDDCode, HDDName, Manufacturer, Price, Capacity, ReadSpeed, WriteSpeed) "
                       "VALUES "
                       "( 'HDD-2','Barracuda 1TB','Seagate',34,1000,173,159),"
                       "( 'HDD-3','Blue 1TB','WD',32,1000,155,138),"
                       "( 'HDD-4','Barracuda 2TB','Seagate',46,2000,164,133),"
                       "( 'HDD-5','Barracuda 3TB','Seagate',70,3000,166,133),"
                       "( 'HDD-6','Black 1TB','WD',73,1000,156,140),"
                       "( 'HDD-7','Barracuda 4TB','Seagate',89,4000,143,123);")
        #Inputting all HDDs here
        db.commit()
        print("HDD table initialised")

    except sqlite3.Error as e:
        db.rollback()
        print(f"Unable to create HDD table. Error: {e}")
        raise e


def create_ssd_table():

    try:
        cursor = db.cursor()

        cursor.execute("DROP TABLE IF EXISTS SSD")

        sql = '''CREATE TABLE IF NOT EXISTS SSD (
                       SSDcode VARCHAR(10) UNIQUE PRIMARY KEY,
                       SSDName VARCHAR(100) NOT NULL,
                       Manufacturer VARCHAR(100) NOT NULL,
                       Price DECIMAL(6,2),
                       Capacity INTEGER,
                       ReadSpeed INTEGER,
                       WriteSpeed INTEGER)
               '''

        cursor.execute(sql)
        cursor.execute("INSERT INTO SSD (SSDCode, SSDName, Manufacturer, Price, Capacity, ReadSpeed, WriteSpeed) "
                       "VALUES "
                       "( 'SSD-2','970 Evo 1TB','Samsung',99,1000,2379,2151),"
                       "( 'SSD-3','970 Evo 500GB','Samsung',66,500,2395,2141),"
                       "( 'SSD-4','EX950 2TB','HP',206,2000,2219,1755),"
                       "( 'SSD-5','970 Evo 250GB','Samsung',50,250,2251,1896);")
        #Inputting all SSDs here
        db.commit()
        print("SSD table initialised")

    except sqlite3.Error as e:
        db.rollback()
        print(f"Unable to create SSD table. Error: {e}")
        raise e


def create_pccase_table():

    try:
        cursor = db.cursor()

        cursor.execute("DROP TABLE IF EXISTS PCCase")

        sql = '''CREATE TABLE IF NOT EXISTS PCCase (
                       Casecode VARCHAR(10) UNIQUE PRIMARY KEY,
                       CaseName VARCHAR(100) NOT NULL,
                       Price DECIMAL(6,2))
               '''

        cursor.execute(sql)
        cursor.execute("INSERT INTO PCCase (Casecode, CaseName, Price) "
                       "VALUES "
                       "('Case-1', 'Corsair SPEC-DELTA Carbide', 44.97),"
                       "('Case-2', 'IONZ KZ08B V2', 29.95),"
                       "('Case-3', 'Corsair 110R', 66.99),"
                       "('Case-4', 'iCUE 4000X', 119.99);")
        #PC Cases are inputted here and some have been directly inputted in the database itself
        db.commit()
        print("Case table initialised")

    except sqlite3.Error as e:
        db.rollback()
        print(f"Unable to create Case table. Error: {e}")
        raise e


def create_mobo_table():

    try:
        cursor = db.cursor()

        cursor.execute("DROP TABLE IF EXISTS Motherboard")

        sql = '''CREATE TABLE IF NOT EXISTS Motherboard (
                       Mobocode VARCHAR(10) UNIQUE PRIMARY KEY,
                       MoboName VARCHAR(100) NOT NULL,
                       Manufacturer VARCHAR(100) NOT NULL,
                       Socket VARCHAR(10),
                       Chipset VARCHAR(10),
                       Price DECIMAL(6,2))
               '''

        cursor.execute(sql)
        cursor.execute("INSERT INTO Motherboard (MoboCode, MoboName, Manufacturer, Socket, Chipset, Price) "
                       "VALUES "
                       "('Mobo-1', 'Gigabyte Z690 Aorus Pro', 'Gigabyte', 'FCLGA1700', 'Z690', 284.70),"
                       "('Mobo-2', 'Asus ROG Maximus XIII Hero', 'Asus', 'FCLGA1200', 'Z590', 434.99),"
                       "('Mobo-3', 'Gigabyte Z590 Aorus Tachyon', 'Gigabyte', 'FCLGA1200', 'Z590', 279.95),"
                       "('Mobo-4', 'MSI Z490 Gaming Plus', 'MSI', 'FCLGA1200', 'Z490', 109.99),"
                       "('Mobo-5', 'MSI MAG B560 Torpedo ATX', 'MSI', 'FCLGA1200', 'B560', 139.85),"
                       "('Mobo-6', 'Asrock B560 Pro4', 'Asrock', 'FCLGA1200', 'B560', 104.99),"
                       "('Mobo-7', 'MSI MAG B660 Tomahawk', 'MSI', 'FCLGA1700', 'B660', 209.99),"
                       "('Mobo-8', 'MSI MPG Z390 Gaming Plus', 'MSI', 'FCLGA1151', 'Z390', 132.22),"
                       "('Mobo-9', 'Gigabyte B450 AORUS Elite', 'Gigabyte', 'AM4', 'B450', 80.99),"
                       "('Mobo-10', 'MSI MPG B550 Gaming Plus', 'MSI', 'AM4', 'B550', 129.99),"
                       "('Mobo-11', 'MSI Meg X570 Ace', 'MSI', 'AM4', 'X570', 383.50),"
                       "('Mobo-12', 'Gigabyte B550 AORUS Elite V2', 'Gigabyte', 'AM4', 'B550', 117.75),"
                       "('Mobo-13', 'MSI X570-A Pro', 'MSI', 'AM4', 'X570', 139.99),"
                       "('Mobo-14', 'Gigabyte B450 Gaming x', 'Gigabyte', 'AM4', 'B450', 65.00),"
                       "('Mobo-15', 'Asus ROG Strix B550-F Gaming', 'Asus', 'AM4', 'B550', 175.00),"
                       "('Mobo-16', 'MSI B450 Tomahawk Max', 'MSI', 'AM4', 'B450', 119.00),"
                       "('Mobo-17', 'Gigabyte A520 AORUS Elite', 'Gigabyte', 'AM4', 'A520', 72.80),"
                       "('Mobo-18', 'MSI X470 Gaming Plus Max', 'MSI', 'AM4', 'X470', 74.99),"
                       "('Mobo-19', 'Asus Prime X470-Pro', 'Asus', 'AM4', 'X470', 124.99),"
                       "('Mobo-20', 'MSI X399 SLI Plus', 'MSI', 'sTR4', 'X399', 269.45),"
                       "('Mobo-21', 'Asrock AMD X399 Phantom Gaming', 'Asrock', 'sTR4', 'X399', 256.29);")

        db.commit()
        print("Mobo table initialised")

    except sqlite3.Error as e:
        db.rollback()
        print(f"Unable to create Mobo table. Error: {e}")
        raise e


def create_ram_table():

    try:
        cursor = db.cursor()

        cursor.execute("DROP TABLE IF EXISTS RAM")

        sql = '''CREATE TABLE IF NOT EXISTS RAM (
                       RAMcode VARCHAR(10) UNIQUE PRIMARY KEY,
                       RAMName VARCHAR(100) NOT NULL,
                       Manufacturer VARCHAR(100) NOT NULL,
                       Price DECIMAL(6,2),
                       Speed INTEGER,
                       StickAmount INTEGER,
                       RAMSize INTEGER)
               '''

        cursor.execute(sql)
        cursor.execute("INSERT INTO RAM (RAMCode, RAMName, Manufacturer, Price, Speed, StickAmount, RAMSize) "
                       "VALUES "
                       "('RAM-1', 'Corsair LPX 16GB', 'Corsair', 65.00, 3600, 2, 16),"
                       "('RAM-2', 'Corsair Vengeance LPX 16GB', 'Corsair', 54.85, 3000, 2, 16),"
                       "('RAM-3', 'G.Skill Ripjaws V 16GB', 'G.Skill', 60.49, 3200, 2, 16),"
                       "('RAM-4', 'Corsair Vengeance LPX 8GB', 'Corsair', 29.49, 2400, 1, 8),"
                       "('RAM-5', 'Corsair Vengeance LPX 32GB', 'Corsair', 84.95, 3200, 2, 32),"
                       "('RAM-6', 'Patriot Viper Steel 32GB', 'Patriot', 99.95, 3600, 2, 32),"
                       "('RAM-7', 'Corsair Vengeance LPX 8GB', 'Corsair', 43.99, 2666, 2, 8),"
                       "('RAM-8', 'Corsair Vengeance LPX 128GB', 'Corsair', 517.99, 2666, 4, 128),"
                       "('RAM-9', 'Corsair Vengeance LPX 256GB', 'Corsair', 2168.99, 2666, 8, 256);")

        db.commit()
        print("RAM table initialised")

    except sqlite3.Error as e:
        db.rollback()
        print(f"Unable to create RAM table. Error: {e}")
        raise e


def create_psu_table():

    try:
        cursor = db.cursor()

        cursor.execute("DROP TABLE IF EXISTS PSU")

        sql = '''CREATE TABLE IF NOT EXISTS PSU (
                       PSUcode VARCHAR(10) UNIQUE PRIMARY KEY,
                       PSUName VARCHAR(100) NOT NULL,
                       Manufacturer VARCHAR(100) NOT NULL,
                       Price DECIMAL(6,2),
                       Power INTEGER,
                       PowerRating VARCHAR(20),
                       isModular VARCHAR(1))
               '''

        cursor.execute(sql)
        cursor.execute("INSERT INTO PSU (PSUCode, PSUName, Manufacturer, Price, Power, PowerRating, isModular) "
                       "VALUES "
                       "('PSU-1', 'Corsair CX650M', 'Corsair', 44.99, 650, 'Bronze', 'N'),"
                       "('PSU-2', 'Corsair CX650F', 'Corsair', 85.02, 650, 'Bronze', 'Y'),"
                       "('PSU-3', 'Corsair TX850M', 'Corsair', 89.99, 850, 'Gold', 'N');")
        #PSUs have been inputted into the database both here and directly into it
        db.commit()
        print("PSU table initialised")

    except sqlite3.Error as e:
        db.rollback()
        print(f"Unable to create PSU table. Error: {e}")
        raise e


def create_cpumobocompatability_table():

    try:
        cursor = db.cursor()

        cursor.execute("DROP TABLE IF EXISTS Compatability")

        sql = '''CREATE TABLE IF NOT EXISTS Compatability (
                       ID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                       CPUCode VARCHAR(10),
                       MoboCode VARCHAR(10),
                       Socket VARCHAR(10),
                       FOREIGN KEY(CPUCode) REFERENCES CPU(CPUcode),
                       FOREIGN KEY(MoboCode) REFERENCES Motherboard(Mobocode))
               '''

        cursor.execute(sql)
        cursor.execute("INSERT INTO Compatability (CPUCode, MoboCode, Socket) "
                       "SELECT CPU.CPUcode, Motherboard.Mobocode, CPU.Socket "
                       "FROM CPU, Motherboard "
                       "WHERE CPU.Socket = Motherboard.Socket")
        #Only takes the CPUCode and MotherboardCodes where the Sockets are the same. The socket is taken from CPU here
        # but it could just as easily have been taken from Motherboard
        db.commit()

        print("Compatibility table initialised")

    except sqlite3.Error as e:
        db.rollback()
        print(f"Unable to create Compatibility table. Error: {e}")
        raise e


def creat_userselection_table():

    try:
        cursor = db.cursor()

        cursor.execute("DROP TABLE IF EXISTS UserSelection")

        sql = '''CREATE TABLE IF NOT EXISTS UserSelection (
                       Username VARCHAR(25) UNIQUE PRIMARY KEY,
                       Budget DECIMAL(6, 2),
                       CPUCode VARCHAR(10),
                       MoboCode VARCHAR(10),
                       GPUCode VARCHAR(10),
                       HDDCode VARCHAR(10),
                       SSDCode VARCHAR(10),
                       CaseCode VARCHAR(10),
                       RAMCode VARCHAR(10),
                       PSUCode VARCHAR(10),
                       FOREIGN KEY(Username) REFERENCES User(Username),
                       FOREIGN KEY(CPUCode) REFERENCES CPU(CPUcode),
                       FOREIGN KEY(MoboCode) REFERENCES Motherboard(Mobocode),
                       FOREIGN KEY(GPUCode) REFERENCES GPU(GPUcode),
                       FOREIGN KEY(HDDCode) REFERENCES HDD(HDDcode),
                       FOREIGN KEY(SSDCode) REFERENCES SSD(SSDcode),
                       FOREIGN KEY(CaseCode) REFERENCES PCCase(Casecode),
                       FOREIGN KEY(RAMCode) REFERENCES RAM(RAMcode),
                       FOREIGN KEY(PSUCode) REFERENCES PSU(PSUcode))
               '''
        #These are all foreign keys since they have been taken from
        #the other tables
        cursor.execute(sql)

        db.commit()
        print("User Selection table initialised")

    except sqlite3.Error as e:
        db.rollback()
        print(f"Unable to create User Selection table. Error: {e}")
        raise e


def init_db():

    confirmation_number = random.randint(100000, 999999)

    print(f"You are erasing all the contents of '{DB_PATH}'.")
    #This is just to stop accidental resettings of the database
    if int(input(f"Please enter this number to continue: '{confirmation_number}': ")) != confirmation_number:
        raise ValueError("Incorrect code.")

    # create_user_table()
    # create_psu_table()
    # create_ssd_table()
    # create_hdd_table()
    # create_gpu_table()
    # create_ram_table()
    # create_mobo_table()
    # create_cpu_table()
    # create_pccase_table()
    # create_cpumobocompatability_table()
    # creat_userselection_table()


if __name__ == '__main__':
    try:
        init_db()

    except Exception as e:
        print(e)




