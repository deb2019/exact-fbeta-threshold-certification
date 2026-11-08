# Prepared-data extension: sources and licences

This file lists the source and stated licence of each of the 71 completed prepared-data tasks (`D000`–`D082`). The machine-readable version is `DATA_SOURCES_PREPARED.csv`. It complements `source_benchmarks/DATA_SOURCES.md`, which covers the UCI datasets of the main experiments.

## How licences were assigned

- **Author description (same prepared file):** licence taken from the author-supplied dataset description sheet for the exact prepared file used (47 tasks).
- **Author description of same source:** the sheet describes a different prepared file derived from the same source dataset; the source licence is applied (6 tasks).
- **UCI repository policy:** the UCI Machine Learning Repository distributes its datasets under CC BY 4.0 (6 tasks, including one obtained through a GitHub mirror of UCI Statlog data). Where the sheet listed a UCI dataset as "Unspecified", the UCI licence is used and the discrepancy is noted.
- **Not provided:** no licence information was supplied (12 tasks). The licence must be checked on the source page before any redistribution.

Licence statements are recorded as supplied or as published by the repository; they are not a legal review. Derived score arrays inherit the obligations of their source licences.

## Redistribution summary

| Redistribution class | Tasks |
|---|---|
| Open: redistribution permitted with attribution | 47 |
| Open, share-alike: attribution; derived data under same licence | 2 |
| Non-commercial: research use with attribution; derived data keep NC terms | 3 |
| Copyleft (AGPL-3.0): redistribution must keep AGPL terms | 2 |
| Unconfirmed: do not redistribute until permission is confirmed | 17 |
| **Total** | **71** |

Prepared input tables are not included in this archive. Saved score/label arrays are included for verification; arrays from tasks in the "Unconfirmed" class should not be publicly redistributed until permission is confirmed.

## Tasks needing a licence check

| ID | Prepared file | Stated licence | Source URL |
|---|---|---|---|
| D010 | Ready Data.csv | Not provided | (none supplied) |
| D011 | CCCD_Prepro_IMB.csv | Not provided | https://www.kaggle.com/datasets/aryashah2k/credit-card-customer-data |
| D019 | preprocessed_loan_approval.csv | Unspecified (see source) | https://www.geeksforgeeks.org/loan-approval-prediction-using-machine-learning/ |
| D020 | preprocessed_loan.csv | Zindi Terms of Use / Challenge Terms (unspecified license) | https://zindi.africa/competitions/data-science-nigeria-challenge-1-loan-default-prediction/data |
| D023 | pre_Loan_dataApp.csv | Unspecified (see source) | https://github.com/prasertcbs/basic-dataset/blob/master/Loan-Approval-Prediction.csv |
| D024 | pre_loan_data.csv | Not provided | https://www.kaggle.com/datasets/taweilo/loan-approval-classification-data |
| D025 | preprocessed_default_fin.csv | Not provided | https://www.kaggle.com/datasets/kmldas/loan-default-prediction |
| D026 | pre_binancecoin_binary.csv | Not provided | https://www.kaggle.com/datasets/sudalairajkumar/cryptocurrencypricehistory |
| D027 | preprocessed_financial_distress.csv | Not provided | https://www.kaggle.com/datasets/shebrahimi/financial-distress |
| D028 | preprocessed_financial_budget.csv | Not provided | https://www.kaggle.com/datasets/mokshithvmok/financial-habits-dataset?select=financial_habits_survey01.csv |
| D029 | preprocessed_income_dataset.csv | Not provided | https://www.kaggle.com/datasets/aradhanahirapara/income-survey-finance-analysis/discussion?sort=hotness |
| D031 | pre_companies_marketvalue.csv | Not provided | https://www.kaggle.com/datasets/soumyodippal000/top-2000-companies-financial-data-2024-dataset |
| D032 | NIFTY500_Imbalanced.csv | Not provided | https://www.kaggle.com/datasets/sudalairajkumar/nifty-indices-dataset |
| D036 | prepro_trade_invest.csv | Not provided | https://www.kaggle.com/datasets/willianoliveiragibin/trade-and-investment |
| D038 | pre_IMB_Insu.csv | Unspecified (see source) | https://www.kaggle.com/code/yasserh/insurance-claim-prediction-top-ml-models/input |
| D040 | pre_ins_imb.csv | Not provided | https://github.com/sharmaroshan/Insurance-Claim-Prediction/blob/master/insurance.csv |
| D054 | preprocessed_training_data.csv | Unspecified (see source) | https://www.kaggle.com/datasets/surekharamireddy/fraudulent-claim-on-cars-physical-damage |

## Data-quality notes

- **D002** (pre_link_phishing_imb.csv): excluded columns: Unnamed: 0; url
- **D003** (pre_healthcare_ransomware.csv): excluded columns: id; attack_date
- **D007** (phishing_imbalanced_40k.csv): every saved validation vector perfectly separates the classes (AUC = 1.0)
- **D011** (CCCD_Prepro_IMB.csv): excluded columns: Avg_Credit_Limit
- **D013** (Credit_preprocessed.csv): author sheet: resampled from source
- **D026** (pre_binancecoin_binary.csv): excluded columns: Open; Close
- **D029** (preprocessed_income_dataset.csv): excluded columns: income_after_tax; Cap_gain; Child_benefit; CPP_QPP; Earning; Guaranteed_income; Investment; Old_age_pension; Private_pension; Self_emp_income; Pension; Self_emp_income.1; Emp_insurance; Salary_wages; compensation
- **D031** (pre_companies_marketvalue.csv): excluded columns: MarketValue_B
- **D033** (audit_risk_preprocessed.csv): excluded columns: Audit_Risk
- **D035** (pre_high_value_cust.csv): excluded columns: TotalSpend; Quantity; UnitPrice; InvoiceNo
- **D036** (prepro_trade_invest.csv): excluded columns: lnx1
- **D037** (TurkishCF_Preprocessed.csv): excluded columns: toplanan_tutar
- **D042** (caravan_preprocessed.csv): Author sheet says "Unspecified"; UCI distributes all repository datasets under CC BY 4.0.
- **D046** (pre_bank_marketing.csv): author sheet: wider leakage-screen set
- **D057** (Pre_Loan_Fraud_Dataset.csv): author sheet: resampled from source; author sheet: wider leakage-screen set; excluded columns: loan_status_Fraudulent - Detected
- **D058** (pre_alzheimers_disease.csv): excluded columns: PatientID; DoctorInCharge
- **D059** (Breast_Cancer_Preprocessed.csv): excluded columns: Survival Months
- **D064** (imbalanced_nhs_dataset.csv): author sheet: one feature had AUC = 1 before exclusions; excluded columns: total_admitted
- **D065** (pre_ovarian_cancer_binary.csv): excluded columns: Timestamp; ProgressionProbability; CancerStage; Histopathology
- **D068** (pre_stroke_risk.csv): author sheet: one feature had AUC = 1 before exclusions; excluded columns: Stroke Risk (%)
- **D070** (support2_preprocessed_binary.csv): excluded columns: slos; surv2m; surv6m; dnr; dnrday; charges; totcst; totmcst
- **D071** (CTG_preprocessed_scaled.csv): excluded columns: b; e; AC; FM; UC; DL; DS; DP; DR; A; B; C; D; E; AD; DE; LD; FS; SUSP
- **D074** (pre_train_fault.csv): author sheet: one feature had AUC = 1 before exclusions; excluded columns: label
- **D075** (ai4i2020_preprocessed.csv): excluded columns: TWF; HDF; PWF; OSF; RNF
- **D080** (ionosphere_preprocessed_corrected.csv): Author sheet says "Unspecified"; UCI distributes all repository datasets under CC BY 4.0.
- **D082** (Final_Healthcare.csv): author sheet: resampled from source

## All tasks

### Cyber-Security

| ID | Prepared file | Source | Licence | Basis |
|---|---|---|---|---|
| D000 | AndroidAdware_Binary_Preprocessed_Final.csv | [Android Malware Detection](https://www.kaggle.com/datasets/subhajournal/android-malware-detection) | AGPL-3.0 | Author description (same prepared file) |
| D001 | ClaMP_Imbalanced.csv | [Classification of Malwares (CLaMP)](https://www.kaggle.com/datasets/saurabhshahane/classification-of-malwares) | CC BY 4.0 | Author description (same prepared file) |
| D002 | pre_link_phishing_imb.csv | [Dataset for Link Phishing Detection](https://www.kaggle.com/datasets/winson13/dataset-for-link-phishing-detection/data) | MIT License | Author description (same prepared file) |
| D003 | pre_healthcare_ransomware.csv | [Healthcare Ransomware Dataset](https://www.kaggle.com/datasets/rivalytics/healthcare-ransomware-dataset/data) | CC BY-SA 4.0 | Author description (same prepared file) |
| D004 | AndroidMalware_Imbalanced.csv | [Malware Detection Dataset](https://www.kaggle.com/datasets/ankit1743/android-malware-detection-dataset) | CC0 1.0 Universal | Author description (same prepared file) |
| D005 | Cybersecurity_WebAttack_Preprocessed_30k.csv | [Network Intrusion Dataset](https://www.kaggle.com/datasets/chethuhn/network-intrusion-dataset) | CC0 1.0 Universal | Author description (same prepared file) |
| D006 | Phishing_Imb_Pre.csv | [Dataset Ready for Malicious URL Detection](https://www.kaggle.com/datasets/pilarpieiro/tabular-dataset-ready-for-malicious-url-detection/data) | Apache 2.0 | Author description (same prepared file) |
| D007 | phishing_imbalanced_40k.csv | [Phishing URL Dataset](https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset) | CC BY 4.0 | Author description (same prepared file) |
| D008 | rt_iot_binary_preprocessed_5037.csv | [Network Traffic Samples](https://archive.ics.uci.edu/dataset/942/rt-iot2022) | CC BY 4.0 | Author description (same prepared file) |

### Finance and Marketing

| ID | Prepared file | Source | Licence | Basis |
|---|---|---|---|---|
| D009 | preprocessed_imbalanced_credit_data.csv | [UCI](https://github.com/JLZml/Credit-Scoring-Data-Sets/blob/master/1.%20UCI%20Repository/Australian/australian.dat) | CC BY 4.0 | Original UCI Statlog (Australian Credit Approval) data obtained via a GitHub mirror; UCI repository policy (all datasets CC BY 4.0) |
| D010 | Ready Data.csv | — | Not provided | No licence information supplied; check source page |
| D011 | CCCD_Prepro_IMB.csv | [https://www.kaggle.com/datasets/aryashah2k/credit-card-customer-data](https://www.kaggle.com/datasets/aryashah2k/credit-card-customer-data) | Not provided | No licence information supplied; check source page |
| D012 | German_preproces.csv | [Statlog German Credit Data](https://www.kaggle.com/datasets/prena0808/statlog-german-credit-data) | CC0 1.0 Universal | Author description (same prepared file) |
| D013 | Credit_preprocessed.csv | [Credit Card Approval Prediction](https://github.com/semasuka/Credit-card-approval-prediction-classification/blob/main/dataset/train.csv) | CC BY 4.0 | Author description (same prepared file) |
| D014 | cc_app_imb.csv | [Credit Card Approval Prediction Dataset](https://github.com/tahsinjahinkhalid/Credit_Card_Approval_Classification/blob/main/data/cc_approval_cleaned.csv) | MIT License | Author description (same prepared file) |
| D017 | crx_imb.csv | [UCI](https://archive.ics.uci.edu/dataset/27/credit+approval) | CC BY 4.0 | UCI repository policy (all datasets CC BY 4.0) |
| D019 | preprocessed_loan_approval.csv | [Loan Approval](https://www.geeksforgeeks.org/loan-approval-prediction-using-machine-learning/) | Unspecified (see source) | Author description (same prepared file) |
| D020 | preprocessed_loan.csv | [Loan Default Prediction Data](https://zindi.africa/competitions/data-science-nigeria-challenge-1-loan-default-prediction/data) | Zindi Terms of Use / Challenge Terms (unspecified license) | Author description (same prepared file) |
| D021 | ready_loan_data.csv | [Loan Approval Dataset](https://www.kaggle.com/datasets/architsharma01/loan-approval-prediction-dataset) | MIT License | Author description (same prepared file) |
| D023 | pre_Loan_dataApp.csv | [Loan Approval Prediction](https://github.com/prasertcbs/basic-dataset/blob/master/Loan-Approval-Prediction.csv) | Unspecified (see source) | Author description (same prepared file) |
| D024 | pre_loan_data.csv | [https://www.kaggle.com/datasets/taweilo/loan-approval-classification-data](https://www.kaggle.com/datasets/taweilo/loan-approval-classification-data) | Not provided | No licence information supplied; check source page |
| D025 | preprocessed_default_fin.csv | [https://www.kaggle.com/datasets/kmldas/loan-default-prediction](https://www.kaggle.com/datasets/kmldas/loan-default-prediction) | Not provided | No licence information supplied; check source page |
| D026 | pre_binancecoin_binary.csv | [https://www.kaggle.com/datasets/sudalairajkumar/cryptocurrencypricehistory](https://www.kaggle.com/datasets/sudalairajkumar/cryptocurrencypricehistory) | Not provided | No licence information supplied; check source page |
| D027 | preprocessed_financial_distress.csv | [https://www.kaggle.com/datasets/shebrahimi/financial-distress](https://www.kaggle.com/datasets/shebrahimi/financial-distress) | Not provided | No licence information supplied; check source page |
| D028 | preprocessed_financial_budget.csv | [https://www.kaggle.com/datasets/mokshithvmok/financial-habits-dataset?select=financial_habits_survey01.csv](https://www.kaggle.com/datasets/mokshithvmok/financial-habits-dataset?select=financial_habits_survey01.csv) | Not provided | No licence information supplied; check source page |
| D029 | preprocessed_income_dataset.csv | [https://www.kaggle.com/datasets/aradhanahirapara/income-survey-finance-analysis/discussion?sort=hotness](https://www.kaggle.com/datasets/aradhanahirapara/income-survey-finance-analysis/discussion?sort=hotness) | Not provided | No licence information supplied; check source page |
| D031 | pre_companies_marketvalue.csv | [https://www.kaggle.com/datasets/soumyodippal000/top-2000-companies-financial-data-2024-dataset](https://www.kaggle.com/datasets/soumyodippal000/top-2000-companies-financial-data-2024-dataset) | Not provided | No licence information supplied; check source page |
| D032 | NIFTY500_Imbalanced.csv | [https://www.kaggle.com/datasets/sudalairajkumar/nifty-indices-dataset](https://www.kaggle.com/datasets/sudalairajkumar/nifty-indices-dataset) | Not provided | No licence information supplied; check source page |
| D033 | audit_risk_preprocessed.csv | [UCI](https://archive.ics.uci.edu/dataset/475/audit+data) | CC BY 4.0 | UCI repository policy (all datasets CC BY 4.0) |
| D034 | ad_preprocessed.csv | [UCI](https://archive.ics.uci.edu/dataset/51/internet+advertisements) | CC BY 4.0 | UCI repository policy (all datasets CC BY 4.0) |
| D035 | pre_high_value_cust.csv | [UCI](https://archive.ics.uci.edu/dataset/352/online+retail) | CC BY 4.0 | UCI repository policy (all datasets CC BY 4.0) |
| D036 | prepro_trade_invest.csv | [https://www.kaggle.com/datasets/willianoliveiragibin/trade-and-investment](https://www.kaggle.com/datasets/willianoliveiragibin/trade-and-investment) | Not provided | No licence information supplied; check source page |
| D037 | TurkishCF_Preprocessed.csv | [UCI](https://archive.ics.uci.edu/dataset/1025/turkish+crowdfunding+startups) | CC BY 4.0 | UCI repository policy (all datasets CC BY 4.0) |
| D038 | pre_IMB_Insu.csv | [Insurance Claim Prediction](https://www.kaggle.com/code/yasserh/insurance-claim-prediction-top-ml-models/input) | Unspecified (see source) | Author description (same prepared file) |
| D039 | pre_ins_fraud.csv | [Insurance Claim Fraud Prediction](https://data.mendeley.com/datasets/992mh7dk9y/2) | CC BY 4.0 | Author description (same prepared file) |
| D040 | pre_ins_imb.csv | [https://github.com/sharmaroshan/Insurance-Claim-Prediction/blob/master/insurance.csv](https://github.com/sharmaroshan/Insurance-Claim-Prediction/blob/master/insurance.csv) | Not provided | No licence information supplied; check source page |
| D042 | caravan_preprocessed.csv | [Insurance Purchased Prediction](https://archive.ics.uci.edu/dataset/125/insurance+company+benchmark+coil+2000) | CC BY 4.0 | Author description of same source (caravan_scaled_pre.csv); this task uses a different prepared file; UCI repository policy (all datasets CC BY 4.0) |
| D044 | pre_telco_churn.csv | [Customer Churn Prediction](https://www.kaggle.com/code/bhartiprasad17/customer-churn-prediction/input) | CC0 1.0 Universal | Author description (same prepared file) |
| D046 | pre_bank_marketing.csv | [Bank Marketing](https://archive.ics.uci.edu/dataset/222/bank+marketing) | CC BY 4.0 | Author description (same prepared file) |
| D048 | customer_churn_preprocessed.csv | [Iranian Churn Dataset](https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset) | CC BY 4.0 | Author description (same prepared file) |
| D049 | online_shoppers_preprocessed.csv | [Online Shoppers Purchasing Intention Dataset](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset.) | CC BY 4.0 | Author description (same prepared file) |

### Fraud / insurance

| ID | Prepared file | Source | Licence | Basis |
|---|---|---|---|---|
| D050 | preprocessed_airbnb_fraud.csv | [Airbnb for Boston with Fraud Detection](https://www.kaggle.com/datasets/hawkingcr/airbnb-for-boston-with-fraud-detection) | AGPL-3.0 (GNU Affero General Public License, version 3) | Author description (same prepared file) |
| D051 | Bank_Transactions_Preprocessed.csv | [Fraud Detection Bank Transction](https://www.kaggle.com/datasets/valakhorasani/bank-transaction-dataset-for-fraud-detection) | Database Contents License (DbCL) v1.0 | Author description (same prepared file) |
| D052 | preprocessed_credit_fraud.csv | [Credit Card Fraud](https://www.kaggle.com/datasets/kartik2112/fraud-detection) | CC0 1.0 Universal | Author description (same prepared file) |
| D053 | CreditCard_Preprocessed.csv | [Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud/data) | CC0 1.0 Universal | Author description (same prepared file) |
| D054 | preprocessed_training_data.csv | [Fraudulent Claim on Cars Physical Damage](https://www.kaggle.com/datasets/surekharamireddy/fraudulent-claim-on-cars-physical-damage) | Unspecified (see source) | Author description (same prepared file) |
| D056 | preprocessed_insu_response.csv | [Insuranec Fraud Claimed](https://www.kaggle.com/datasets/arashnic/imbalanced-data-practice) | CC0 1.0 Universal | Author description (same prepared file) |
| D057 | Pre_Loan_Fraud_Dataset.csv | [Loan Application & Transaction Fraud Detection](https://www.kaggle.com/datasets/prajwaldongre/loan-application-and-transaction-fraud-detection) | CC0 1.0 Universal | Author description (same prepared file) |
| D082 | Final_Healthcare.csv | [Healthcare Providers Data For Anomaly Detection](https://www.kaggle.com/datasets/tamilsel/healthcare-providers-data) | Database Contents License (DbCL) v1.0 | Author description (same prepared file) |

### Maintenance / other

| ID | Prepared file | Source | Licence | Basis |
|---|---|---|---|---|
| D073 | Helicopter_Anomaly_dataset.csv | [Anomaly Detection in Helicopter](https://www.kaggle.com/datasets/nagasai524/anomaly-detection-in-helicopter/data) | CC BY-NC 4.0 | Author description (same prepared file) |
| D074 | pre_train_fault.csv | [High-Speed Train Bogie Vibration & Fault Diagnosis](https://www.kaggle.com/datasets/ziya07/high-speed-train-bogie-vibration-and-fault-diagnosis) | CC0 1.0 Universal | Author description (same prepared file) |
| D075 | ai4i2020_preprocessed.csv | [Machine Failure Computer Numerical Control](https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset) | CC BY 4.0 | Author description (same prepared file) |
| D076 | Annealing_Binary_Preprocessed.csv | [Annealing](https://archive.ics.uci.edu/dataset/3/annealing) | CC BY 4.0 | Author description (same prepared file) |
| D077 | aps_failure_reduced_30k.csv | [Aps Failure](https://archive.ics.uci.edu/dataset/421/aps+failure+at+scania+trucks) | CC BY 4.0 | Author description (same prepared file) |
| D078 | pop_failures_binary_preprocessed.csv | [Climate Model Simulation Crashes](https://archive.ics.uci.edu/dataset/252/climate+model+simulation+crashes) | CC BY 4.0 | Author description of same source (pop_failures_converted_positive_class.csv); this task uses a different prepared file |
| D079 | HTRU_2_preprocessed.csv | [Anomaly detection of Pulser System (HTRU2)](https://archive.ics.uci.edu/dataset/372/htru2) | CC BY 4.0 | Author description (same prepared file) |
| D080 | ionosphere_preprocessed_corrected.csv | [Ionosphere](https://archive.ics.uci.edu/dataset/52/ionosphere) | CC BY 4.0 | Author description (same prepared file); UCI repository policy (all datasets CC BY 4.0) |
| D081 | MITBIH_ECG_Binary_Preprocessed.csv | [Anomaly Detection with CNN Autoencoders](https://www.kaggle.com/code/redpen12/anomaly-detection-with-cnn-autoencoders/input) | Open Data Commons Attribution License (ODC-By) v1.0 | Author description (same prepared file) |

### Medical

| ID | Prepared file | Source | Licence | Basis |
|---|---|---|---|---|
| D058 | pre_alzheimers_disease.csv | [Alzheimers](https://www.kaggle.com/datasets/rabieelkharoua/alzheimers-disease-dataset) | CC BY 4.0 | Author description (same prepared file) |
| D059 | Breast_Cancer_Preprocessed.csv | [Breast Cancer Prediction](https://www.kaggle.com/datasets/marshalpatel3558/breast-cancer-prediction) | Apache 2.0 | Author description (same prepared file) |
| D060 | preprocessed_diabetes_data.csv | [Diabetes Health Indicators](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset) | CC BY 4.0 | Author description of same source (Diabetes_Preprocessed.csv); this task uses a different prepared file |
| D061 | Healthy_Lifestyle_Imbalanced.csv | [Healthy Lifestyle](https://www.kaggle.com/datasets/aditibabu/healthy-lifestyle) | CC0 1.0 Universal | Author description (same prepared file) |
| D062 | LengthOfStay_Preprocessed.csv | [Hospital Length of Stay Dataset Microsoft](https://www.kaggle.com/datasets/aayushchou/hospital-length-of-stay-dataset-microsoft) | MIT License | Author description of same source (LengthOfStay_Binary_Imbalanced_50K.csv); this task uses a different prepared file |
| D063 | ICU_Death_Prediction_Preprocessed.csv | [ICU Patient Outcome Prediction](https://www.kaggle.com/datasets/fdemoribajolin/death-classification-icu) | CC BY-NC-SA 4.0 | Author description (same prepared file) |
| D064 | imbalanced_nhs_dataset.csv | [NHS Admissions Data 2011 2020](https://www.kaggle.com/datasets/tomfarnell/nhs-admissions-data-2011-2020) | MIT License | Author description of same source (nhs_highly_imbalanced_scaled.csv); this task uses a different prepared file |
| D065 | pre_ovarian_cancer_binary.csv | [Ovarian Cancer Risk and Progression Data](https://www.kaggle.com/datasets/datasetengineer/ovarian-cancer-risk-and-progression-data) | CC BY-NC-SA 4.0 | Author description of same source (ovarian_dataset_smaller.csv); this task uses a different prepared file |
| D067 | parkinsons_highly_imbalanced.csv | [Parkinson Disease](https://www.kaggle.com/datasets/porinitahoque/parkinsons-disease-pd-data-analysis) | ODbL 1.0 (Open Data Commons Open Database License 1.0) | Author description (same prepared file) |
| D068 | pre_stroke_risk.csv | [Stroke Risk](https://www.kaggle.com/datasets/mahatiratusher/stroke-risk-prediction-dataset) | MIT License | Author description (same prepared file) |
| D069 | preprocessed_stunting_sampled_10k.csv | [Stunting Wasting Dataset](https://www.kaggle.com/datasets/jabirmuktabir/stunting-wasting-dataset) | Apache 2.0 | Author description (same prepared file) |
| D070 | support2_preprocessed_binary.csv | [Support Health Data for Death Prediction](https://archive.ics.uci.edu/dataset/880/support2) | CC BY 4.0 | Author description (same prepared file) |
| D071 | CTG_preprocessed_scaled.csv | [Cardiotocography Dataset](https://archive.ics.uci.edu/dataset/193/cardiotocography) | CC BY 4.0 | Author description (same prepared file) |
