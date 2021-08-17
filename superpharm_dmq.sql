--
--Insert Addresses Table
--
INSERT INTO Addresses (address1, address2, city, state, zip)
VALUES (:address1Input, :address2Input, :cityInput, :stateInput, :zipInput);

--
--Delete from Addresses Table
--
DELETE FROM Addresses WHERE addressID = :addressIDInput;

--
--Update Addresses Table
--
UPDATE Addresses 
SET address1 = :address1Input, address2 = :address2Input, city = :cityInput, state = :stateInput, zip = :zipInput
WHERE addressID = :addressIDInput;

--
--Generate Addresses Table
--
SELECT * FROM Addresses;


--
--Insert Patients Table
--
INSERT INTO Patients (firstName, lastName, birthDate, phoneNumber, addressID)
VALUES (:firstNameInput, :lastNameInput, :birthDateInput, :phoneNumberInput, :addressIDInput);

--
--Delete from Patients Table
--
DELETE FROM Patients WHERE patientID = :patientIDInput;

--
--Update Patients Table
--
UPDATE Patients 
SET firstName = :firstNameInput, lastName = :lastNameInput, birthDate = :birthDateInput, phoneNumber = :phoneNumberInput, addressID = :addressIDInput
WHERE id = :patientIDInput;

--
--Generate Patients Table
--
SELECT * FROM Patients;

--
--Filter Patients table
--
SELECT * FROM Patients
WHERE :filterCategory = :filterInput;


--
--Insert Healthcare_Providers Table
--
INSERT INTO Healthcare_Providers (nationalProviderIdentifier, firstName, lastName, specialty)
VALUES (:nationalProviderIdentifierInput, :firstNameInput, :lastNameInput, :specialtyInput);

--
--Delete from Healthcare_Providers Table
--
DELETE FROM Healthcare_Providers WHERE nationalProviderIdentifier = :nationalProviderIdentifierInput;

--
--Update Healthcare_Providers Table
--
UPDATE Healthcare_Providers 
SET nationalProviderIdentifier = nationalProviderIdentifierInput, firstName = :firstNameInput, lastName = :lastNameInput, specialty = :specialtyInput
WHERE id = :nationalProviderIdentifierInput;

--
--Generate Healthcare_Providers Table
--
SELECT * FROM Healthcare_Providers;


--Insert Patients_Providers Table
--
INSERT INTO Patients_Providers (nationalProviderIdentifier, patientID)
VALUES (:nationalProviderIdentifierInput, :patientIDInput);

--
--Delete Patients_Providers Table
--
DELETE FROM Patients_Providers 
WHERE nationalProviderIdentifier = :nationalProviderIdentifierInput
AND patientID = :patientIDInput;

--
--Update Patients_Providers Table
--
UPDATE Patients_Providers 
SET nationalProviderIdentifier = :nationalProviderIdentifierInput, patientID = :patientIDInput
WHERE nationalProviderIdentifier = :nationalProviderIdentifierInput AND patientID = :patientIDInput;

--
--Generate Patients_Providers Table
--
SELECT * FROM Patients_Providers;

--
--Generate Expanded Patient_Providers Table
--
SELECT Patients.patientID, Patients.firstName, Patients.lastName, Patients_Providers.nationalProviderIdentifier,
Healthcare_Providers.firstName, Healthcare_Providers.lastName, Healthcare_Providers.specialty
FROM Patients
LEFT JOIN Patients_Providers
ON Patients.patientID = Patients_Providers.patientID
LEFT JOIN Healthcare_Providers
ON Patients_Providers.nationalProviderIdentifier = Healthcare_Providers.nationalProviderIdentifier;


--
--Insert Drugs Table
--
INSERT INTO Drugs (nationalDrugCode, genericName, brandName, strength, quantityAvailable)
VALUES (:nationalDrugCodeInput, :genericNameInput, :brandNameInput, :strengthInput, :quantityAvailableInput);

--
--Delete from Drugs Table
--
DELETE FROM Drugs WHERE nationalDrugCode = :nationalDrugCodeInput;

--
--Update Drugs Table
--
UPDATE Drugs 
SET nationalDrugCode = :nationalDrugCodeInput, genericName = :genericNameInput, brandName = :brandNameInput, strength = :strengthInput, quantityAvailable = :quantityAvailableInput
WHERE nationalDrugCode = :nationalDrugCodeInput;

--
--Generate Drugs Table
--
SELECT * FROM Drugs;


--
--Insert Prescriptions Table
--
INSERT INTO Prescriptions (shipDate, patientID, nationalProviderIdentifier, nationalDrugCode)
VALUES (:shipDateInput, :patientIDInput, :nationalProviderIdentifierInput, :nationalDrugCodeInput);

--
--Delete from Prescriptions Table
--
DELETE FROM Prescriptions WHERE scriptID = :scriptIDInput;

--
--Update Prescriptions Table
--
UPDATE Prescriptions 
SET shipDate = :shipDateInput, patientID = :patientIDInput, nationalProviderIdentifier = :nationalProviderIdentifierInput, nationalDrugCode = :nationalDrugCodeInput
WHERE scriptID = :scriptIDInput;

--
--Generate Prescriptions Table
--
SELECT * FROM Prescriptions;

--
--Generate Expanded Prescriptions Table
--

SELECT Prescriptions.scriptID, Prescriptions.shipDate, Patients.patientID, Patients.firstName, Patients.lastName, Healthcare_Providers.nationalProviderIdentifier,
Healthcare_Providers.firstName AS prfirstName, Healthcare_Providers.lastName AS prlastName, Healthcare_Providers.specialty, Drugs.genericName, Drugs.brandName, Drugs.strength
FROM Prescriptions
LEFT JOIN Patients
ON Prescriptions.patientID = Patients.patientID
LEFT JOIN Healthcare_Providers
ON Prescriptions.nationalProviderIdentifier = Healthcare_Providers.nationalProviderIdentifier
LEFT JOIN Drugs
ON Prescriptions.nationalDrugCode = Drugs.nationalDrugCode;