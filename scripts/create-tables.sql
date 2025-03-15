create database dw;

create schema stg;

create table dw.stg.stg_department (
    departmentid INT,
    name VARCHAR(255),
    groupname VARCHAR(255),
    modifieddate TIMESTAMP,
    last_update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table dw.stg.stg_employee (
	businessentityid int,
	nationalidnumber varchar(15),
	loginid varchar(256),
	jobtitle varchar(50),
	birthdate date,
	maritalstatus bpchar(1),
	gender bpchar(1),
	hiredate date,
	salariedflag varchar(50),
	vacationhours int2 DEFAULT 0,
	sickleavehours int2 DEFAULT 0,
	currentflag varchar(50),
	rowguid varchar(100),
	modifieddate timestamp,
	organizationnode varchar,
	last_update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table dw.stg.stg_employeedepartmenthistory (
	businessentityid int,
	departmentid int,
	shiftid int,
	startdate date,
	enddate date,
	modifieddate timestamp,
	last_update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table dw.stg.stg_employeepayhistory (
	businessentityid int,
	ratechangedate timestamp,
	rate numeric,
	payfrequency int,
	modifieddate timestamp,
	last_update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP	
);

create table dw.stg.stg_productvendor (
	productid int,
	businessentityid int,
	averageleadtime int,
	standardprice numeric, 
	lastreceiptcost numeric,
	lastreceiptdate timestamp,
	minorderqty int,
	maxorderqty int,
	onorderqty int,
	unitmeasurecode bpchar(3),
	modifieddate timestamp,
	last_update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table dw.stg.stg_countryregioncurrency (
	countryregioncode varchar(3),
	currencycode bpchar(3),
	modifieddate timestamp,
	last_update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP	
);

create table dw.stg.stg_culture (
	cultureid bpchar(6),
	name varchar(500),
	modifieddate timestamp,
	last_update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table dw.stg.stg_location (
	locationid serial4,
	name varchar(500),
	costrate numeric,
	availability numeric(8, 2),
	modifieddate timestamp,
	last_update_date timestamp DEFAULT now() NOT NULL
);

create table dw.stg.stg_product (
	productid serial4,
	name varchar(500),
	productnumber varchar(25),
	makeflag varchar(10),
	finishedgoodsflag varchar(10),
	color varchar(15),
	safetystocklevel int2 ,
	reorderpoint int2,
	standardcost numeric,
	listprice numeric,
	"size" varchar(5),
	sizeunitmeasurecode bpchar(3),
	weightunitmeasurecode bpchar(3),
	weight numeric(8, 2),
	daystomanufacture int4,
	productline bpchar(2),
	"class" bpchar(2),
	"style" bpchar(2),
	productsubcategoryid int4,
	productmodelid int4,
	sellstartdate timestamp,
	sellenddate timestamp,
	discontinueddate timestamp,
	rowguid varchar(500),
	modifieddate timestamp,
	last_update_date timestamp DEFAULT now() NOT NULL
);

create table dw.stg.stg_productcategory (
	productcategoryid serial4,
	name varchar(500),
	rowguid varchar(500),
	modifieddate timestamp,
	last_update_date timestamp DEFAULT now() NOT NULL
);

create table dw.stg.stg_productdescription (
	productdescriptionid serial4,
	description varchar(400),
	rowguid varchar(500),
	modifieddate timestamp,
	last_update_date timestamp DEFAULT now() NOT NULL
);

create table dw.stg.stg_productreview (
	productreviewid serial4,
	productid int4,
	reviewername varchar(200),
	reviewdate timestamp,
	emailaddress varchar(50),
	rating int4,
	comments varchar(3850),
	modifieddate timestamp,
	last_update_date timestamp DEFAULT now() NOT NULL
);