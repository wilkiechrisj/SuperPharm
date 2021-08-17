/*Dropping all tables*/
DROP TABLE IF EXISTS Prescriptions;
DROP TABLE IF EXISTS Drugs;
DROP TABLE IF EXISTS Patients_Providers;
DROP TABLE IF EXISTS Healthcare_Providers;
DROP TABLE IF EXISTS Patients;
DROP TABLE IF EXISTS Addresses;

/* Table structure for Addresses Table */
CREATE TABLE Addresses (
    addressID INT NOT NULL UNIQUE AUTO_INCREMENT,
    address1 VARCHAR(255) NOT NULL,
    address2 VARCHAR(255),
    city VARCHAR(255) NOT NULL,
    state CHAR(2) NOT NULL,
    zip CHAR(5) NOT NULL,
    PRIMARY KEY (addressID)
);
/* Dumping data for Addresses Table*/
LOCK TABLES Addresses WRITE;

INSERT INTO Addresses (address1, city, state, zip)
VALUES ('123 New City Lane', 'Redlands' , 'CA', '92374');

INSERT INTO Addresses (address1, address2, city, state, zip)
VALUES ('456 Old Town Road', 'PO Box 24400', 'Lyons' , 'CO', '80540');

INSERT INTO Addresses (address1, city, state, zip)
VALUES ('98 Happy Valley Road', 'Jamesburg' , 'NJ', '08831');

UNLOCK TABLES;



/* Table structure for Patients Table */
CREATE TABLE Patients (
    patientID INT NOT NULL UNIQUE AUTO_INCREMENT,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    birthDate DATE NOT NULL,
    phoneNumber VARCHAR(20) NOT NULL,
    addressID INT,
    PRIMARY KEY (patientID),
    FOREIGN KEY (addressID) REFERENCES Addresses(addressID)
);
/* Dumping data for Patients Table*/
LOCK TABLES Patients WRITE;

INSERT INTO Patients (firstName, lastName, birthDate, phoneNumber, addressID)
VALUES ('Old', 'Lady', '1945-01-06', '15555555555', 1);

INSERT INTO Patients (firstName, lastName, birthDate, phoneNumber, addressID)
VALUES ('Young', 'Claus', '2008-12-25', '12345678910', 2);

INSERT INTO Patients (firstName, lastName, birthDate, phoneNumber, addressID)
VALUES ('Vincent', 'Adultman', '1980-05-11', '9876543201', 3);

UNLOCK TABLES;



/*Table structure for Healthcare_Providers Table*/
CREATE TABLE Healthcare_Providers (
    nationalProviderIdentifier CHAR(10) NOT NULL UNIQUE,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    specialty VARCHAR(255) NOT NULL,
    PRIMARY KEY (nationalProviderIdentifier)
);
/* Dumping data for Healthcare_Providers Table*/
LOCK TABLES Healthcare_Providers WRITE;

INSERT INTO Healthcare_Providers (nationalProviderIdentifier, firstName, lastName, specialty)
VALUES ('1659662732', 'Doctor', 'Hearts', 'Cardiology');

INSERT INTO Healthcare_Providers (nationalProviderIdentifier, firstName, lastName, specialty)
VALUES ('1235237355', 'Katy', 'Scan', 'Radiology');

INSERT INTO Healthcare_Providers (nationalProviderIdentifier, firstName, lastName, specialty)
VALUES ('1699299883', 'Doc', 'Cutz', 'Surgery');

UNLOCK TABLES;



/* Table structure for Patients_Providers Table*/
CREATE TABLE Patients_Providers (
    patientID INT NOT NULL,
    nationalProviderIdentifier CHAR(10) NOT NULL,
    PRIMARY KEY (patientID, nationalProviderIdentifier),
    FOREIGN KEY (patientID) REFERENCES Patients(patientID),
    FOREIGN KEY (nationalProviderIdentifier) REFERENCES Healthcare_Providers(nationalProviderIdentifier)
);
/* Dumping data for Patients_Providers Table*/
LOCK TABLES Patients_Providers WRITE;

INSERT INTO Patients_Providers (nationalProviderIdentifier, patientID)
VALUES ('1659662732', 1);

INSERT INTO Patients_Providers (nationalProviderIdentifier, patientID)
VALUES ('1659662732', 2);

INSERT INTO Patients_Providers (nationalProviderIdentifier, patientID)
VALUES ('1699299883', 3);

UNLOCK TABLES;



/* Table structure for Drugs Table*/
CREATE TABLE Drugs (
    nationalDrugCode CHAR(12) NOT NULL UNIQUE,
    genericName VARCHAR(255) NOT NULL,
    brandName VARCHAR(255) NOT NULL,
    strength VARCHAR(255) NOT NULL,
    quantityAvailable INT NOT NULL,
    PRIMARY KEY (nationalDrugCode)
);
/* Dumping data for Drugs Table */
LOCK TABLES Drugs WRITE;

INSERT INTO Drugs (nationalDrugCode, genericName, brandName, strength, quantityAvailable)
VALUES ('0074-0067-02', 'adalimumab', 'Humira', '40mg/0.8ml', 48);

INSERT INTO Drugs (nationalDrugCode, genericName, brandName, strength, quantityAvailable)
VALUES ('58406-446-04', 'etanercept', 'Enbrel', '50mg/ml', 60);

INSERT INTO Drugs (nationalDrugCode, genericName, brandName, strength, quantityAvailable)
VALUES ('57894-060-02', 'ustekinumab', 'Stelara', '45mg/0.5ml', 100);

UNLOCK TABLES;



/* Table structure for Prescriptions Table*/
CREATE TABLE Prescriptions (
    scriptID INT NOT NULL UNIQUE AUTO_INCREMENT,
    shipDate DATE,
    patientID INT NOT NULL,
    nationalDrugCode CHAR(12) NOT NULL,
    nationalProviderIdentifier CHAR(10) NOT NULL,
    PRIMARY KEY (scriptID),
    FOREIGN KEY (patientID) REFERENCES Patients(patientID),
    FOREIGN KEY (nationalProviderIdentifier) REFERENCES Healthcare_Providers(nationalProviderIdentifier),
    FOREIGN KEY (nationalDrugCode) REFERENCES Drugs(nationalDrugCode)
);
/* Dumping data for Precriptions Table*/
LOCK TABLES Prescriptions WRITE;

INSERT INTO Prescriptions (shipDate, patientID, nationalDrugCode, nationalProviderIdentifier)
VALUES ('2021-07-25', 1, '0074-0067-02', '1659662732');

INSERT INTO Prescriptions (shipDate, patientID, nationalDrugCode, nationalProviderIdentifier)
VALUES ('2021-07-26', 2, '58406-446-04', '1659662732');

INSERT INTO Prescriptions (patientID, nationalDrugCode, nationalProviderIdentifier)
VALUES (3, '57894-060-02', '1699299883');

UNLOCK TABLES;