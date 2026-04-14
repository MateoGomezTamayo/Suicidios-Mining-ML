# Formal Project Proposal

## Big Data and Data Mining for Risk Profile Identification in Suicide Attempt Records

**Author:** [Student name]  
**Program:** [Academic program name]  
**Course:** [Course name]  
**Institution:** Institucion Universitaria Salazar y Herrera  
**Date:** April 2026

## 1. Introduction

Public health data analytics has become essential to understand complex phenomena, identify vulnerable populations, and support decision-making. In this context, suicide attempt records are a high-value data source because they allow the study of demographic, social, clinical, and territorial factors associated with risk behavior.

However, the analytical value of these records depends on two key conditions. First, an infrastructure capable of storing and processing large data volumes in an efficient and scalable way. Second, analytical techniques that transform raw data into actionable knowledge. In other words, moving and cleaning data is not enough; it must be interpreted, modeled, and converted into useful evidence.

This proposal integrates two complementary approaches. On one side, it defines an AWS-based Big Data architecture for ingestion, transformation, storage, and querying of the SIVIGILA suicide attempt dataset. On the other side, it applies CRISP-DM as a formal framework for data mining to identify risk profiles, territorial patterns, and relevant factors.

This integration creates a unified solution where Big Data is the technological backbone and data mining is the knowledge-generation mechanism. The project goes beyond a technical pipeline and focuses on an analytical solution with potential value for epidemiological surveillance and prevention.

## 2. Problem Statement

The growing availability of epidemiological and administrative health records has increased the need for technological solutions that can process data efficiently. In suicide attempt monitoring, surveillance records include valuable information to analyze trends, associated factors, and high-risk population profiles. However, these records are often dispersed, heterogeneous, or not structured for analytical use.

From a data engineering perspective, the challenge is to build a processing flow that can ingest, clean, transform, and expose data in a scalable way. From an analytical perspective, the challenge is to apply data mining techniques that discover non-obvious relationships, segment profiles, and support risk assessment processes.

These two perspectives are often handled separately, creating a gap between infrastructure and modeling. As a result, opportunities for end-to-end analytical value are lost.

Research question: **How can an AWS Big Data architecture be integrated with data mining techniques to identify risk profiles and relevant patterns in SIVIGILA suicide attempt records?**

## 3. Justification

This project is relevant from three dimensions:

1. Technical: it consolidates a data-processing architecture based on AWS services (Amazon S3, AWS Glue, AWS Step Functions, and Amazon Athena) organized in Bronze, Silver, and Gold layers.
2. Academic: it aligns the Big Data proposal with CRISP-DM and formal data mining practices.
3. Social: it addresses a critical public-health issue by providing analytical tools to identify vulnerable groups, high-incidence zones, and associated risk factors.

Therefore, integrating Big Data and data mining is both feasible and necessary to move from infrastructure-focused work to applied analytics that can support decisions.

## 4. Objectives

### 4.1 General Objective

Design and implement an integrated Big Data and data mining solution to process suicide attempt records, identify risk profiles, and generate analytical knowledge for prevention and epidemiological surveillance.

### 4.2 Specific Objectives

1. Build an AWS data pipeline with Bronze, Silver, and Gold architecture for SIVIGILA data.
2. Standardize, clean, and transform data to improve quality and analytical availability.
3. Build Gold-layer analytical tables for epidemiological querying and modeling.
4. Apply CRISP-DM phases from business understanding to evaluation.
5. Identify risk-related variables, territorial patterns, and vulnerable population profiles.
6. Evaluate classification or segmentation models that provide useful evidence for interpretation.

## 5. Conceptual and Methodological Framework

The proposal is based on the complementarity between Big Data and data mining. Big Data provides scalable storage, transformation, and query capabilities, while data mining extracts patterns, relationships, and actionable knowledge.

The architecture uses AWS services: S3 as data lake, Glue for ETL, Step Functions for orchestration, and Athena for analytics queries. The pipeline is structured into Bronze (raw ingestion), Silver (clean and standardized data), and Gold (analytics-ready enriched data).

CRISP-DM is used as the methodological framework: business understanding, data understanding, preparation, modeling, evaluation, and deployment.

## 6. Proposed Solution

The solution integrates a Big Data architecture and a data mining strategy in one workflow. Raw suicide attempt data is stored in Bronze. A first Glue ETL process transforms it into Silver, applying cleaning, column normalization, null handling, duplicate control, and validation.

A second Glue ETL process builds Gold analytical outputs. Two key structures are generated:

1. A municipality-year summary table for descriptive and territorial analysis.
2. An individual risk-profile table combining demographic and risk variables into a risk score and analytical label.

These Gold tables become the basis for classification or segmentation modeling.

## 7. Data and Variables of Interest

The dataset includes variables such as age, sex, municipality, hospitalization, prior history, attempt method, and psychosocial or clinical factors.

Descriptive analysis supports group-level patterns (age, sex, municipality, time), while explanatory and predictive analysis supports associations and model development for differentiated risk profiles.

## 8. Development Methodology

Development follows CRISP-DM phases aligned with the AWS architecture.

1. Business understanding: define analytical problem, key questions, and expected value.
2. Data understanding: exploratory analysis, type review, null/duplicate/outlier checks.
3. Data preparation: encoding, transformation, feature selection, and scaling when needed.
4. Modeling: train classification (Logistic Regression, Decision Tree, Random Forest) or segmentation (K-Means) models.
5. Evaluation: use task-specific metrics (accuracy, precision, recall, F1, ROC-AUC, Silhouette).
6. Deployment: leave analytical outputs query-ready in Athena and optionally expose dashboards.

## 9. Scope

The project includes ingestion, cleaning, transformation, and organization of SIVIGILA records in AWS, plus data mining workflows for pattern discovery and risk profiling.

Out of scope: clinical production deployment, real-time integration with healthcare providers, and full MLOps implementation.

## 10. Expected Results

Expected outputs include a reproducible AWS health-data pipeline, reliable analytical tables, and evidence of relevant patterns and risk profiles.

Academically, the project aims to demonstrate methodological and technical coherence in combining Big Data and data mining. Practically, it provides analytical inputs for interpretation and future studies.

## 11. Preliminary Conclusions

The key strength of this proposal is the integration of two dimensions that are usually developed separately: data infrastructure and advanced analytics. Big Data becomes the foundation for interpretable analytical processes, while data mining benefits from a scalable and structured data backbone.

## 12. Suggested Final Title

**Big Data and Data Mining for Risk Profile Identification in Suicide Attempt Records Using AWS and CRISP-DM**