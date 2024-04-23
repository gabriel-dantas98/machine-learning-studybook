
CREATE TABLE "production" (
	"id" serial NOT NULL,
	"product" varchar(255),
	"year" timestamp,
	"category" varchar(255),
	"quantity" float,
	PRIMARY KEY("id")
);

/**
KG
*/
CREATE TABLE "processing" (
	"id" serial NOT NULL,
	"product" varchar(255),
	"quantity" float,
	"year" date,
	"category" varchar(255),
	PRIMARY KEY("id")
);

CREATE TABLE "commercialization" (
	"id" serial NOT NULL,
	"product" varchar(255),
	"year" timestamp,
	"category" varchar(255),
	"quantity" float,
	PRIMARY KEY("id")
);

CREATE TABLE "exporting" (
	"id" serial NOT NULL,
	"countries" varchar(255),
	"year" timestamp,
	"quantity" float,
	"value" float,
	PRIMARY KEY("id")
);

CREATE TABLE "importing" (
	"id" serial NOT NULL,
	"countries" varchar(255),
	"year" timestamp,
	"quantity" float,
	"value" float,
	PRIMARY KEY("id")
);

