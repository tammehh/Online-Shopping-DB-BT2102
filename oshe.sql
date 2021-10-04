DROP TABLE IF EXISTS Customers;
CREATE TABLE Customers(
	CustomerID CHAR(10) NOT NULL,
    CustomerName VARCHAR(100) NOT NULL,
    Address VARCHAR(100) NOT NULL,
	Gender CHAR(1) CHECK(Gender IN("M","F")), 
    EmailAddress VARCHAR(100) NOT NULL,
    PhoneNumber VARCHAR(20) NOT NULL,
    Password VARCHAR(100) NOT NULL,
    PRIMARY KEY (CustomerID));

DROP TABLE IF EXISTS Administrator;
CREATE TABLE Administrator (
	AdministratorID CHAR(10) NOT NULL, 
	AdminName VARCHAR(100) NOT NULL, 
	Gender CHAR(1) CHECK(Gender IN("M","F")),
	PhoneNumber VARCHAR(20) NOT NULL,
	Password VARCHAR(100) NOT NULL,
	PRIMARY KEY(AdministratorID)
);
    
DROP TABLE IF EXISTS Item;
CREATE TABLE Item(
	ItemID  CHAR(4) NOT NULL,
    CustomerID CHAR(10), 
    PurchaseDate DATE, 
    Model VARCHAR(10) CHECK(Model IN ("Light1", "Light2", "SmartHome1", "Safe1", "Safe2", "Safe3")),
    ProductID CHAR(3) NOT NULL,
    PurchaseStatus VARCHAR(6) CHECK(PurchaseStatus IN ("Sold", "Unsold")),
    ServiceStatus VARCHAR(30) CHECK(ServiceStatus IN ("Waiting For Approval", "In progress", "Completed")),
    PowerSupply VARCHAR(7) Check(PowerSupply IN ("USB","Battery")),
    Factory VARCHAR(100) NOT NULl,
    Color VARCHAR(20) NOT NULL,
    ProductionYear CHAR(4) NOT NULL,
    PRIMARY KEY (ItemID),
    FOREIGN KEY(ProductID) REFERENCES ModelType (ProductID),
    FOREIGN KEY(CustomerID) REFERENCES Customers (CustomerID)
    );
    
DROP TABLE IF EXISTS ModelType;
CREATE TABLE ModelType(
	ProductID Char(3) CHECK(ProductID IN ("001","002","003","004","005","006","007")),
	Model VARCHAR(10) CHECK(Model IN ("Light1", "Light2", "SmartHome1", "Safe1", "Safe2", "Safe3")),
	Category VARCHAR(6) CHECK(Category IN ("Lights", "Locks")),
	CostPrice DECIMAL(5,2) NOT NULL,
	Warranty INT NOT NULL,
	PRIMARY KEY(ProductID)
 );

    
DROP TABLE IF EXISTS Request;
CREATE TABLE Request(
	RequestID CHAR(10) NOT NULL, 
	CustomerID CHAR(10) NOT NULL, 
	RequestStatus VARCHAR(100) CHECK(RequestStatus IN ("N/A", "Submitted", "Submitted and Waiting for payment", "In progress", "Approved" , "Cancelled")) NOT NULL,
	RequestDate DATE NOT NULL,
	PRIMARY KEY(RequestID),
	FOREIGN KEY(CustomerID) REFERENCES Customers (CustomerID)
);
    
DROP TABLE IF EXISTS ServiceFee;
CREATE TABLE ServiceFee(
	CustomerID CHAR(10) NOT NULL, 
	RequestID CHAR(10) NOT NULL, 
	ServiceFee Decimal(5,2) NOT NULL, 
	SettlementDate DATE,
	CreationDate DATE NOT NULL,
	FOREIGN KEY(CustomerID) REFERENCES Customers (CustomerID),
	FOREIGN KEY(RequestID) REFERENCES Request (RequestID)
);
    
DROP TABLE IF EXISTS Service;
CREATE TABLE Service(
	AdministratorID CHAR(10) NOT NULL, 
	RequestID CHAR(10) NOT NULL,
	ServiceStatus VARCHAR(30) CHECK(ServiceStatus IN ("N/A", "Waiting for approval", "In progress", "Completed")),
	FOREIGN KEY(AdministratorID) REFERENCES Administrator (AdministratorID),
	FOREIGN KEY(RequestID) REFERENCES Request (RequestID)  
);
