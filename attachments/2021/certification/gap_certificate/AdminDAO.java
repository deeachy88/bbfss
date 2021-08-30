// 
// Decompiled by Procyon v0.5.36
// 

package bt.gov.dhps.framework.dao;

import bt.gov.dhps.framework.VO.UserRolePriviledge;
import bt.gov.dhps.dto.DatabaseConfigDTO;
import bt.gov.framework.web.exception.DatabaseUtil;
import bt.gov.dhps.framework.web.actionForm.ReportFormBean;
import bt.gov.dhps.framework.dto.ReportDTO;
import java.text.DecimalFormat;
import java.text.ParseException;
import bt.gov.dhps.framework.util.HPSConstants;
import bt.gov.dhps.framework.VO.ApplicationDataVO;
import java.text.SimpleDateFormat;
import bt.gov.dhps.framework.VO.MasterVO;
import bt.gov.dhps.framework.VO.MenuVO;
import bt.gov.dhps.framework.util.PasswordEncryptionUtil;
import java.sql.SQLException;
import bt.gov.dhps.framework.dto.AdminDTO;
import bt.gov.framework.web.exception.HPSSystemException;
import java.sql.ResultSet;
import java.sql.PreparedStatement;
import java.sql.Connection;
import bt.gov.framework.web.exception.HPSException;
import bt.gov.dhps.framework.util.ConnectionManager;
import java.util.ArrayList;
import bt.gov.dhps.framework.dto.UserDTO;
import java.util.List;
import java.sql.Date;

public class AdminDAO
{
    private static AdminDAO adminDAO;
    private static Date date;
    private static final String GET_MONTHLY_ENERGY_SALE_FOR_OVERALL = "SELECT a.Plant_Name, a.Year, MONTHNAME(STR_TO_DATE(a.Month, '%M')) MONTHNAME,MONTH(STR_TO_DATE(a.Month, '%M'))numericMonth,  a.Month, a.Generation, a.Export_MU, a.Sale_To_BPC_MU, a.Export_Tariff, a.Domestic_Tariff, a.Revenue_From_Export, a.Revenue_From_BPC FROM t_monthly_data_dgpc a WHERE a.Year = ?  GROUP BY a.Plant_Id,MONTH(STR_TO_DATE(a.Month, '%M')) ORDER BY a.Plant_Id,MONTH(STR_TO_DATE(a.Month, '%M'))";
    private static final String GET_MONTHLY_ENERGY_SALE_FOR_ALLHYDROPLANT = "SELECT a.Plant_Name, a.Year, MONTHNAME(STR_TO_DATE(a.Month, '%M')) MONTHNAME,MONTH(STR_TO_DATE(a.Month, '%M'))numericMonth,a.Month, a.Generation, a.Generation, a.Export_MU, a.Sale_To_BPC_MU, a.Export_Tariff, a.Domestic_Tariff, a.Revenue_From_Export, a.Revenue_From_BPC FROM t_monthly_data_dgpc a WHERE a.Month =? AND  a.Year = ? GROUP BY a.Plant_Id";
    private static final String GET_MONTHLY_ENERGY_SALE_FOR_ALLMONTH = "SELECT a.Plant_Name, a.Year, MONTHNAME(STR_TO_DATE(a.Month, '%M')) MONTHNAME,MONTH(STR_TO_DATE(a.Month, '%M'))numericMonth,a.Month, a.Generation, a.Export_MU, a.Sale_To_BPC_MU, a.Export_Tariff, a.Domestic_Tariff, a.Revenue_From_Export, a.Revenue_From_BPC FROM t_monthly_data_dgpc a WHERE a.Plant_Id=? AND  a.Year = ? ORDER BY MONTH(STR_TO_DATE(a.Month, '%M'))";
    private static final String GET_MONTHLY_ENERGY_SALE = "SELECT a.Plant_Name, a.Year, MONTHNAME(STR_TO_DATE(a.Month, '%M')) MONTHNAME,MONTH(STR_TO_DATE(a.Month, '%M'))numericMonth,a.Month, a.Generation, a.Export_MU,a .Sale_To_BPC_MU, a.Export_Tariff, a.Domestic_Tariff, a.Revenue_From_Export, a.Revenue_From_BPC FROM t_monthly_data_dgpc a WHERE a.Plant_Id=? AND a.Month =? AND a.Year = ?";
    private static final String MONTH_AND_QUATERLY_ENERGY_SALE_FOR_ALL_MONTH = "SELECT a.Year, MONTHNAME(STR_TO_DATE(a.Month, '%M')) MONTHNAME,MONTH(STR_TO_DATE(a.Month, '%M'))numericMonth,  a.Month, SUM(a.Generation)AS Generation, SUM(a.Revenue_From_Export)AS Revenue_From_Export  , SUM(a.Revenue_From_BPC) AS Revenue_From_BPC, SUM(a.Revenue_From_Export+a.Revenue_From_BPC) AS total FROM t_monthly_data_dgpc a WHERE a.Year=? GROUP BY a.Month  ORDER BY MONTH(STR_TO_DATE(a.Month, '%M'));";
    private static final String generatequaterly = "SELECT d.Year, MONTHNAME(STR_TO_DATE(d.Month, '%M')) MONTHNAME,MONTH(STR_TO_DATE(d.Month, '%M'))numericMonth,d.Month, d.Generation, d.Revenue_From_Export, d.Revenue_From_BPC, SUM(d.Revenue_From_Export+d.Revenue_From_BPC) total FROM t_monthly_data_dgpc d WHERE d.Plant_Id=? AND d.Year=? GROUP BY d.Month  ORDER BY MONTH(STR_TO_DATE(d.Month, '%M'))";
    private static final String MONTHLY_ENERGY_PURCHASE_BY_BPC_ALL_MONTH = "SELECT  a.`Plant_Name`, \ta.`Energy_Purchase_MU`, \ta.`Energy_Purchase_Payment`, \ta.`Energy_wheeled_MU`, \ta.`Energy_wheeled_Revenue`, \ta.`Energy_Sale_Mu`, \ta.`Energy_Sale_Revenue` FROM `t_bpc_energy_purchase2`a WHERE a.`Data_Year`=?;";
    private static final String MONTHLY_ENERGY_PURCHASE_BY_BPC = "SELECT  a.`Plant_Name`, \ta.`Energy_Purchase_MU`, \ta.`Energy_Purchase_Payment`, \ta.`Energy_wheeled_MU`, \ta.`Energy_wheeled_Revenue`, \ta.`Energy_Sale_Mu`, \ta.`Energy_Sale_Revenue` FROM `t_bpc_energy_purchase2`a WHERE a.`Data_Month`=? AND a.`Data_Year`=?;";
    private static final String WIND_POWER_PLANT_ENERGY_GENERATION_FOR_ALL_MONTH = "SELECT a.Year, a.`Plant_Name`, \tSUM(a.T1_Energy_Generated) AS T1_Energy_Generated, \tSUM(a.T2_Energy_Generated) AS T2_Energy_Generated, \tSUM(a.Total_Energy_Generated) AS Total_Energy_Generated, \tSUM(a.`T1_Machine_Availability(hrs)`) AS T1_Machine_Availability, \tSUM(a.`T2_Machine_Availability(hrs)`)AS T2_Machine_Availability \tFROM `t_monthly_wind_power` a WHERE a.`Year`=?;";
    private static final String WIND_POWER_PLANT_ENERGY_GENERATION_FOR_ALL_MONTHWISE = "SELECT a.Year, a.`Plant_Name`, \tSUM(T1_Energy_Generated) AS T1_Energy_Generated, \tSUM(T2_Energy_Generated) AS T2_Energy_Generated, \tSUM(Total_Energy_Generated) AS Total_Energy_Generated, \tSUM(a.`T1_Machine_Availability(hrs)`) AS T1_Machine_Availability, \tSUM(a.`T2_Machine_Availability(hrs)`)AS T2_Machine_Availability \tFROM `t_monthly_wind_power` a WHERE a.`Month`=? AND  a.`Year`=?;";
    private static final String GET_REPORT_ON_NUMBER_OF_CONSUMER_MONTHWISE = "SELECT t.Data_Year, ROUND(((Total_Low_Vol_Ru/Grand_Total)*100),2) LVRpercent ,        ROUND(((Total_Low_Vol_Ru_Coo/Grand_Total)*100),2)  Ru_Coo_percent,        ROUND(((Total_Low_Vol_Ru_MT/Grand_Total)*100) ,2) Ru_MT_percent,        ROUND(((Total_Low_Vol_Ru_CL/Grand_Total)*100),2)  Ru_CL_percent,        ROUND(((Total_Low_Vol_Urban /Grand_Total)*100),2)  Urban_percent,        ROUND(((Total_Low_Vol_RI /Grand_Total)*100),2)  RI_percent,        ROUND(((Low_Vol_B3_Com/Grand_Total)*100),2) Com_percent,        ROUND(((Low_Vol_B3_Ind/Grand_Total)*100),2) Ind_percent,        ROUND(((Low_Vol_B3_Agr/Grand_Total)*100),2) Agr_percent,        ROUND(((Low_Vol_B3_Ins/Grand_Total)*100),2) Ins_percent,        ROUND(((Low_Vol_B3_SL/Grand_Total)*100),2) SL_percent,        ROUND(((Low_Vol_B3_PHA/Grand_Total)*100),2) PHA_percent,        ROUND(((Low_Vol_B3_TC /Grand_Total)*100),2) TC_percent,        ROUND(((LV_Bulk_B3/Grand_Total)*100),2) LV_Bulk_percent,        ROUND(((Med_Vol_B3/Grand_Total)*100),2) Med_Vol_B3_percent,        ROUND(((High_Vol_B3 /Grand_Total)*100),2) High_Vol_B3_percent,        Total_Low_Vol_Ru,        Total_Low_Vol_Ru_Coo,        Total_Low_Vol_Ru_MT,        Total_Low_Vol_Ru_CL,        Total_Low_Vol_Urban ,        Total_Low_Vol_RI,        Low_Vol_B3_Com ,        Low_Vol_B3_Ind ,        Low_Vol_B3_Agr ,        Low_Vol_B3_Ins ,        Low_Vol_B3_SL ,        Low_Vol_B3_PHA ,        Low_Vol_B3_TC ,        LV_Bulk_B3 ,        Med_Vol_B3 ,        High_Vol_B3 ,        Grand_Total       FROM (SELECT a.Data_Year,(SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) )AS Total_Low_Vol_Ru, \t\t(SUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)) AS Total_Low_Vol_Ru_Coo , \t\t(SUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT))AS Total_Low_Vol_Ru_MT , \t\t(SUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL ))AS Total_Low_Vol_Ru_CL , \t\t(SUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)) AS Total_Low_Vol_Urban , \t\t(SUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) )AS Total_Low_Vol_RI , \t\tSUM(Low_Vol_B3_Com)AS Low_Vol_B3_Com , \t\tSUM(Low_Vol_B3_Ind)AS Low_Vol_B3_Ind , \t\tSUM(Low_Vol_B3_Agr) AS Low_Vol_B3_Agr , \t\tSUM(Low_Vol_B3_Ins)AS Low_Vol_B3_Ins , \t\tSUM(Low_Vol_B3_SL)AS Low_Vol_B3_SL , \t\tSUM(Low_Vol_B3_PHA) AS Low_Vol_B3_PHA , \t\tSUM(Low_Vol_B3_TC)AS Low_Vol_B3_TC , \t\tSUM(LV_Bulk_B3)AS LV_Bulk_B3 , \t\tSUM(Med_Vol_B3)AS Med_Vol_B3 , \t\tSUM(High_Vol_B3) AS High_Vol_B3 , \t    (SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) + \t\tSUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)+ \t\tSUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT)+ \t\tSUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL )+ \t\tSUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)+ \t\tSUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) + \t\tSUM(Low_Vol_B3_Com)+ \t\tSUM(Low_Vol_B3_Ind)+ \t\tSUM(Low_Vol_B3_Agr)+ \t\tSUM(Low_Vol_B3_Ins)+ \t\tSUM(Low_Vol_B3_SL)+ \t\tSUM(Low_Vol_B3_PHA)+ \t\tSUM(Low_Vol_B3_TC)+ \t\tSUM(LV_Bulk_B3)+ \t\tSUM(Med_Vol_B3)+ \t\tSUM(High_Vol_B3)) AS Grand_Total \t\tFROM  `t_bpc_number_of_customers_dzongkhag_wise2` \t\ta WHERE a.`Dzongkhag_Id`=? AND a.`Data_Month`=? AND a.`Data_Year`=?) t";
    private static final String GET_REPORT_ON_NUMBER_OF_CONSUMER_FOR_ALL_DZONGKHAG = "SELECT t.Data_Year,ROUND(((Total_Low_Vol_Ru/Grand_Total)*100),2) LVRpercent , ROUND(((Total_Low_Vol_Ru_Coo/Grand_Total)*100),2)  Ru_Coo_percent, ROUND(((Total_Low_Vol_Ru_MT/Grand_Total)*100) ,2) Ru_MT_percent, ROUND(((Total_Low_Vol_Ru_CL/Grand_Total)*100),2)  Ru_CL_percent, ROUND(((Total_Low_Vol_Urban /Grand_Total)*100),2)  Urban_percent, ROUND(((Total_Low_Vol_RI /Grand_Total)*100),2)  RI_percent, ROUND(((Low_Vol_B3_Com/Grand_Total)*100),2) Com_percent, ROUND(((Low_Vol_B3_Ind/Grand_Total)*100),2) Ind_percent, ROUND(((Low_Vol_B3_Agr/Grand_Total)*100),2) Agr_percent, ROUND(((Low_Vol_B3_Ins/Grand_Total)*100),2) Ins_percent, ROUND(((Low_Vol_B3_SL/Grand_Total)*100),2) SL_percent, ROUND(((Low_Vol_B3_PHA/Grand_Total)*100),2) PHA_percent, ROUND(((Low_Vol_B3_TC /Grand_Total)*100),2) TC_percent, ROUND(((LV_Bulk_B3/Grand_Total)*100),2) LV_Bulk_percent, ROUND(((Med_Vol_B3/Grand_Total)*100),2) Med_Vol_B3_percent, ROUND(((High_Vol_B3 /Grand_Total)*100),2) High_Vol_B3_percent, Total_Low_Vol_Ru, Total_Low_Vol_Ru_Coo, Total_Low_Vol_Ru_MT, Total_Low_Vol_Ru_CL, Total_Low_Vol_Urban , Total_Low_Vol_RI, Low_Vol_B3_Com , Low_Vol_B3_Ind , Low_Vol_B3_Agr , Low_Vol_B3_Ins , Low_Vol_B3_SL , Low_Vol_B3_PHA , Low_Vol_B3_TC , LV_Bulk_B3 , Med_Vol_B3 , High_Vol_B3 , Grand_Total FROM (SELECT a.Data_Year,(SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) )AS Total_Low_Vol_Ru, (SUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)) AS Total_Low_Vol_Ru_Coo , (SUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT))AS Total_Low_Vol_Ru_MT , (SUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL ))AS Total_Low_Vol_Ru_CL , (SUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)) AS Total_Low_Vol_Urban , (SUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) )AS Total_Low_Vol_RI , SUM(Low_Vol_B3_Com)AS Low_Vol_B3_Com , SUM(Low_Vol_B3_Ind)AS Low_Vol_B3_Ind , SUM(Low_Vol_B3_Agr) AS Low_Vol_B3_Agr , SUM(Low_Vol_B3_Ins)AS Low_Vol_B3_Ins , SUM(Low_Vol_B3_SL)AS Low_Vol_B3_SL , SUM(Low_Vol_B3_PHA) AS Low_Vol_B3_PHA , SUM(Low_Vol_B3_TC)AS Low_Vol_B3_TC , SUM(LV_Bulk_B3)AS LV_Bulk_B3 , SUM(Med_Vol_B3)AS Med_Vol_B3 , SUM(High_Vol_B3) AS High_Vol_B3 , (SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) + SUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo) + SUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT) + SUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL )+ SUM(Low_Vol_B1_Urban)  +SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban) + SUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI)  + SUM(Low_Vol_B3_Com) + SUM(Low_Vol_B3_Ind) + SUM(Low_Vol_B3_Agr) + SUM(Low_Vol_B3_Ins) + SUM(Low_Vol_B3_SL) + SUM(Low_Vol_B3_PHA) + SUM(Low_Vol_B3_TC) + SUM(LV_Bulk_B3) + SUM(Med_Vol_B3) + SUM(High_Vol_B3)) AS Grand_Total FROM  `t_bpc_number_of_customers_dzongkhag_wise2` a WHERE  a.`Data_Month`=? AND a.`Data_Year`=?) t;";
    private static final String GET_REPORT_ON_ENERGY_UTILIZATION_FOR_OVERALL = "SELECT t.Data_Year, ROUND(((Total_Low_Vol_Ru/Grand_Total)*100),2) LVRpercent , \t\t      ROUND(((Total_Low_Vol_Ru_Coo/Grand_Total)*100),2)  Ru_Coo_percent, \t\t      ROUND(((Total_Low_Vol_Ru_MT/Grand_Total)*100) ,2) Ru_MT_percent, \t\t      ROUND(((Total_Low_Vol_Ru_CL/Grand_Total)*100),2)  Ru_CL_percent, \t\t      ROUND(((Total_Low_Vol_Urban /Grand_Total)*100),2)  Urban_percent, \t\t      ROUND(((Total_Low_Vol_RI /Grand_Total)*100),2)  RI_percent, \t\t      ROUND(((Low_Vol_B3_Com/Grand_Total)*100),2) Com_percent, \t\t      ROUND(((Low_Vol_B3_Ind/Grand_Total)*100),2) Ind_percent, \t\t      ROUND(((Low_Vol_B3_Agr/Grand_Total)*100),2) Agr_percent, \t\t      ROUND(((Low_Vol_B3_Ins/Grand_Total)*100),2) Ins_percent, \t\t      ROUND(((Low_Vol_B3_SL/Grand_Total)*100),2) SL_percent, \t\t      ROUND(((Low_Vol_B3_PHA/Grand_Total)*100),2) PHA_percent, \t\t      ROUND(((Low_Vol_B3_TC /Grand_Total)*100),2) TC_percent, \t\t      ROUND(((LV_Bulk_B3/Grand_Total)*100),2) LV_Bulk_percent, \t\t      ROUND(((Med_Vol_B3/Grand_Total)*100),2) Med_Vol_B3_percent, \t\t      ROUND(((High_Vol_B3 /Grand_Total)*100),2) High_Vol_B3_percent, \t\t      Total_Low_Vol_Ru, \t\t      Total_Low_Vol_Ru_Coo, \t\t      Total_Low_Vol_Ru_MT, \t\t      Total_Low_Vol_Ru_CL, \t\t      Total_Low_Vol_Urban , \t\t      Total_Low_Vol_RI, \t\t      Low_Vol_B3_Com , \t\t      Low_Vol_B3_Ind , \t\t      Low_Vol_B3_Agr , \t\t      Low_Vol_B3_Ins , \t\t      Low_Vol_B3_SL , \t\t      Low_Vol_B3_PHA , \t\t      Low_Vol_B3_TC , \t\t      LV_Bulk_B3 , \t\t      Med_Vol_B3 , \t\t      High_Vol_B3 , \t\t      Grand_Total \t\t       FROM (SELECT a.Data_Year,(SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) )AS Total_Low_Vol_Ru, \t\t \t\t(SUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)) AS Total_Low_Vol_Ru_Coo , \t\t        (SUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT))AS Total_Low_Vol_Ru_MT , \t\t\t\t(SUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL ))AS Total_Low_Vol_Ru_CL , \t\t \t\t(SUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)) AS Total_Low_Vol_Urban , \t\t\t\t(SUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) )AS Total_Low_Vol_RI , \t\t\t\tSUM(Low_Vol_B3_Com)AS Low_Vol_B3_Com , \t\t\t\tSUM(Low_Vol_B3_Ind)AS Low_Vol_B3_Ind , \t\t\t\tSUM(Low_Vol_B3_Agr) AS Low_Vol_B3_Agr , \t\t\t\tSUM(Low_Vol_B3_Ins)AS Low_Vol_B3_Ins , \t\t\t\tSUM(Low_Vol_B3_SL)AS Low_Vol_B3_SL , \t\t \t\tSUM(Low_Vol_B3_PHA) AS Low_Vol_B3_PHA , \t\t\t    SUM(Low_Vol_B3_TC)AS Low_Vol_B3_TC , \t\t  \t\tSUM(LV_Bulk_B3)AS LV_Bulk_B3 , \t\t \t\tSUM(Med_Vol_B3)AS Med_Vol_B3 , \t\t \t\tSUM(High_Vol_B3) AS High_Vol_B3 , \t\t\t    (SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) + \t\t\t\tSUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)+ \t\t \t\tSUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT)+ \t\t\t\tSUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL )+ \t\t \t\tSUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)+ \t\t\t\tSUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) + \t\t  \t\tSUM(Low_Vol_B3_Com)+ \t\t \t\tSUM(Low_Vol_B3_Ind)+ \t\t  \t\tSUM(Low_Vol_B3_Agr)+ \t\t \t\tSUM(Low_Vol_B3_Ins)+ \t\t \t\tSUM(Low_Vol_B3_SL)+ \t\t\t\tSUM(Low_Vol_B3_PHA)+ \t\t \t\tSUM(Low_Vol_B3_TC)+ \t\t\t    SUM(LV_Bulk_B3)+ \t\t\t\tSUM(Med_Vol_B3)+ \t\t\t    SUM(High_Vol_B3)) AS Grand_Total \t\t \t\tFROM `t_bpc_energy_utilization_dzongkhag_wise2` a \t\t\t\tWHERE a.`Data_Year`=?) t;";
    private static final String GET_REPORT_ON_ENERGY_UTILIZATION_FOR_DZONGKHAG = "SELECT t.Data_Year,ROUND(((Total_Low_Vol_Ru/Grand_Total)*100),2) LVRpercent , \t      ROUND(((Total_Low_Vol_Ru_Coo/Grand_Total)*100),2)  Ru_Coo_percent, \t      ROUND(((Total_Low_Vol_Ru_MT/Grand_Total)*100) ,2) Ru_MT_percent, \t      ROUND(((Total_Low_Vol_Ru_CL/Grand_Total)*100),2)  Ru_CL_percent, \t      ROUND(((Total_Low_Vol_Urban /Grand_Total)*100),2)  Urban_percent, \t      ROUND(((Total_Low_Vol_RI /Grand_Total)*100),2)  RI_percent, \t      ROUND(((Low_Vol_B3_Com/Grand_Total)*100),2) Com_percent, \t      ROUND(((Low_Vol_B3_Ind/Grand_Total)*100),2) Ind_percent, \t      ROUND(((Low_Vol_B3_Agr/Grand_Total)*100),2) Agr_percent, \t      ROUND(((Low_Vol_B3_Ins/Grand_Total)*100),2) Ins_percent, \t      ROUND(((Low_Vol_B3_SL/Grand_Total)*100),2) SL_percent, \t      ROUND(((Low_Vol_B3_PHA/Grand_Total)*100),2) PHA_percent, \t      ROUND(((Low_Vol_B3_TC /Grand_Total)*100),2) TC_percent, \t      ROUND(((LV_Bulk_B3/Grand_Total)*100),2) LV_Bulk_percent, \t      ROUND(((Med_Vol_B3/Grand_Total)*100),2) Med_Vol_B3_percent, \t      ROUND(((High_Vol_B3 /Grand_Total)*100),2) High_Vol_B3_percent, \t      Total_Low_Vol_Ru, \t      Total_Low_Vol_Ru_Coo, \t      Total_Low_Vol_Ru_MT, \t      Total_Low_Vol_Ru_CL, \t      Total_Low_Vol_Urban , \t      Total_Low_Vol_RI, \t      Low_Vol_B3_Com , \t      Low_Vol_B3_Ind , \t      Low_Vol_B3_Agr , \t      Low_Vol_B3_Ins , \t      Low_Vol_B3_SL , \t      Low_Vol_B3_PHA , \t      Low_Vol_B3_TC , \t      LV_Bulk_B3 , \t      Med_Vol_B3 , \t      High_Vol_B3 , \t      Grand_Total \t     FROM (SELECT a.Data_Year,(SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) )AS Total_Low_Vol_Ru, \t\t \t\t(SUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)) AS Total_Low_Vol_Ru_Coo , \t\t  \t\t(SUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT))AS Total_Low_Vol_Ru_MT , \t\t\t\t(SUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL ))AS Total_Low_Vol_Ru_CL , \t\t  \t\t(SUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)) AS Total_Low_Vol_Urban , \t\t \t\t(SUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) )AS Total_Low_Vol_RI , \t\t\t\tSUM(Low_Vol_B3_Com)AS Low_Vol_B3_Com , \t\t \t\tSUM(Low_Vol_B3_Ind)AS Low_Vol_B3_Ind , \t\t \t\tSUM(Low_Vol_B3_Agr) AS Low_Vol_B3_Agr , \t\t\t\tSUM(Low_Vol_B3_Ins)AS Low_Vol_B3_Ins , \t\t  \t\tSUM(Low_Vol_B3_SL)AS Low_Vol_B3_SL , \t\t \t\tSUM(Low_Vol_B3_PHA) AS Low_Vol_B3_PHA , \t\t \t\tSUM(Low_Vol_B3_TC)AS Low_Vol_B3_TC , \t\t  \t\tSUM(LV_Bulk_B3)AS LV_Bulk_B3 , \t\t  \t\tSUM(Med_Vol_B3)AS Med_Vol_B3 , \t\t  \t\tSUM(High_Vol_B3) AS High_Vol_B3 , \t\t \t    (SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) + \t\t \t\tSUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)+ \t\t\t\tSUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT)+ \t\t \t\tSUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL )+ \t\t  \t\tSUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)+ \t\t  \t\tSUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) + \t\t  \t\tSUM(Low_Vol_B3_Com)+ \t\t  \t\tSUM(Low_Vol_B3_Ind)+ \t\t  \t\tSUM(Low_Vol_B3_Agr)+ \t\t  \t\tSUM(Low_Vol_B3_Ins)+ \t\t  \t\tSUM(Low_Vol_B3_SL)+ \t\t \t\tSUM(Low_Vol_B3_PHA)+ \t\t  \t\tSUM(Low_Vol_B3_TC)+ \t\t  \t\tSUM(LV_Bulk_B3)+ \t\t  \t\tSUM(Med_Vol_B3)+ \t\t \t\tSUM(High_Vol_B3)) AS Grand_Total \t\t \t\tFROM `t_bpc_energy_utilization_dzongkhag_wise2` a \t\t  \t\tWHERE a.`Data_Month`=? AND a.`Data_Year`=?) t;";
    private static final String GET_REPORT_ON_ENERGY_UTILIZATION_FOR_ALL_MONTH = " SELECT t.Data_Year, ROUND(((Total_Low_Vol_Ru/Grand_Total)*100),2) LVRpercent ,        ROUND(((Total_Low_Vol_Ru_Coo/Grand_Total)*100),2)  Ru_Coo_percent,        ROUND(((Total_Low_Vol_Ru_MT/Grand_Total)*100) ,2) Ru_MT_percent,        ROUND(((Total_Low_Vol_Ru_CL/Grand_Total)*100),2)  Ru_CL_percent,        ROUND(((Total_Low_Vol_Urban /Grand_Total)*100),2)  Urban_percent,        ROUND(((Total_Low_Vol_RI /Grand_Total)*100),2)  RI_percent,        ROUND(((Low_Vol_B3_Com/Grand_Total)*100),2) Com_percent,        ROUND(((Low_Vol_B3_Ind/Grand_Total)*100),2) Ind_percent,        ROUND(((Low_Vol_B3_Agr/Grand_Total)*100),2) Agr_percent,        ROUND(((Low_Vol_B3_Ins/Grand_Total)*100),2) Ins_percent,        ROUND(((Low_Vol_B3_SL/Grand_Total)*100),2) SL_percent,        ROUND(((Low_Vol_B3_PHA/Grand_Total)*100),2) PHA_percent,        ROUND(((Low_Vol_B3_TC /Grand_Total)*100),2) TC_percent,        ROUND(((LV_Bulk_B3/Grand_Total)*100),2) LV_Bulk_percent,        ROUND(((Med_Vol_B3/Grand_Total)*100),2) Med_Vol_B3_percent,        ROUND(((High_Vol_B3 /Grand_Total)*100),2) High_Vol_B3_percent,        Total_Low_Vol_Ru,        Total_Low_Vol_Ru_Coo,        Total_Low_Vol_Ru_MT,        Total_Low_Vol_Ru_CL,        Total_Low_Vol_Urban ,        Total_Low_Vol_RI,        Low_Vol_B3_Com ,        Low_Vol_B3_Ind ,        Low_Vol_B3_Agr ,        Low_Vol_B3_Ins ,        Low_Vol_B3_SL ,        Low_Vol_B3_PHA ,        Low_Vol_B3_TC ,        LV_Bulk_B3 ,        Med_Vol_B3 ,        High_Vol_B3 ,        Grand_Total       FROM (SELECT a.Data_Year,(SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) )AS Total_Low_Vol_Ru, \t\t(SUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)) AS Total_Low_Vol_Ru_Coo , \t\t(SUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT))AS Total_Low_Vol_Ru_MT , \t\t(SUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL ))AS Total_Low_Vol_Ru_CL , \t\t(SUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)) AS Total_Low_Vol_Urban , \t\t(SUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) )AS Total_Low_Vol_RI , \t\tSUM(Low_Vol_B3_Com)AS Low_Vol_B3_Com , \t\tSUM(Low_Vol_B3_Ind)AS Low_Vol_B3_Ind , \t\tSUM(Low_Vol_B3_Agr) AS Low_Vol_B3_Agr , \t\tSUM(Low_Vol_B3_Ins)AS Low_Vol_B3_Ins , \t\tSUM(Low_Vol_B3_SL)AS Low_Vol_B3_SL , \t\tSUM(Low_Vol_B3_PHA) AS Low_Vol_B3_PHA , \t\tSUM(Low_Vol_B3_TC)AS Low_Vol_B3_TC , \t\tSUM(LV_Bulk_B3)AS LV_Bulk_B3 , \t\tSUM(Med_Vol_B3)AS Med_Vol_B3 , \t\tSUM(High_Vol_B3) AS High_Vol_B3 , \t    (SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) + \t\tSUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)+ \t\tSUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT)+ \t\tSUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL )+ \t\tSUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)+ \t\tSUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) + \t\tSUM(Low_Vol_B3_Com)+ \t\tSUM(Low_Vol_B3_Ind)+ \t\tSUM(Low_Vol_B3_Agr)+ \t\tSUM(Low_Vol_B3_Ins)+ \t\tSUM(Low_Vol_B3_SL)+ \t\tSUM(Low_Vol_B3_PHA)+ \t\tSUM(Low_Vol_B3_TC)+ \t\tSUM(LV_Bulk_B3)+ \t\tSUM(Med_Vol_B3)+ \t\tSUM(High_Vol_B3)) AS Grand_Total \t\tFROM `t_bpc_energy_utilization_dzongkhag_wise2` a \t\tWHERE a.`Dzongkhag_Id`=? AND a.`Data_Year`=?) t";
    private static final String GET_REPORT_ON_ENERGY_UTILIZATION = "SELECT  t.Data_Year,ROUND(((Total_Low_Vol_Ru/Grand_Total)*100),2) LVRpercent ,        ROUND(((Total_Low_Vol_Ru_Coo/Grand_Total)*100),2)  Ru_Coo_percent,        ROUND(((Total_Low_Vol_Ru_MT/Grand_Total)*100) ,2) Ru_MT_percent,        ROUND(((Total_Low_Vol_Ru_CL/Grand_Total)*100),2)  Ru_CL_percent,        ROUND(((Total_Low_Vol_Urban /Grand_Total)*100),2)  Urban_percent,        ROUND(((Total_Low_Vol_RI /Grand_Total)*100),2)  RI_percent,        ROUND(((Low_Vol_B3_Com/Grand_Total)*100),2) Com_percent,        ROUND(((Low_Vol_B3_Ind/Grand_Total)*100),2) Ind_percent,        ROUND(((Low_Vol_B3_Agr/Grand_Total)*100),2) Agr_percent,        ROUND(((Low_Vol_B3_Ins/Grand_Total)*100),2) Ins_percent,        ROUND(((Low_Vol_B3_SL/Grand_Total)*100),2) SL_percent,        ROUND(((Low_Vol_B3_PHA/Grand_Total)*100),2) PHA_percent,        ROUND(((Low_Vol_B3_TC /Grand_Total)*100),2) TC_percent,        ROUND(((LV_Bulk_B3/Grand_Total)*100),2) LV_Bulk_percent,        ROUND(((Med_Vol_B3/Grand_Total)*100),2) Med_Vol_B3_percent,        ROUND(((High_Vol_B3 /Grand_Total)*100),2) High_Vol_B3_percent,        Total_Low_Vol_Ru,        Total_Low_Vol_Ru_Coo,        Total_Low_Vol_Ru_MT,        Total_Low_Vol_Ru_CL,        Total_Low_Vol_Urban ,        Total_Low_Vol_RI,        Low_Vol_B3_Com ,        Low_Vol_B3_Ind ,        Low_Vol_B3_Agr ,        Low_Vol_B3_Ins ,        Low_Vol_B3_SL ,        Low_Vol_B3_PHA ,        Low_Vol_B3_TC ,        LV_Bulk_B3 ,        Med_Vol_B3 ,        High_Vol_B3 ,        Grand_Total       FROM (SELECT a.Data_Year,(SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) )AS Total_Low_Vol_Ru, \t\t(SUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)) AS Total_Low_Vol_Ru_Coo , \t\t(SUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT))AS Total_Low_Vol_Ru_MT , \t\t(SUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL ))AS Total_Low_Vol_Ru_CL , \t\t(SUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)) AS Total_Low_Vol_Urban , \t\t(SUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) )AS Total_Low_Vol_RI , \t\tSUM(Low_Vol_B3_Com)AS Low_Vol_B3_Com , \t\tSUM(Low_Vol_B3_Ind)AS Low_Vol_B3_Ind , \t\tSUM(Low_Vol_B3_Agr) AS Low_Vol_B3_Agr , \t\tSUM(Low_Vol_B3_Ins)AS Low_Vol_B3_Ins , \t\tSUM(Low_Vol_B3_SL)AS Low_Vol_B3_SL , \t\tSUM(Low_Vol_B3_PHA) AS Low_Vol_B3_PHA , \t\tSUM(Low_Vol_B3_TC)AS Low_Vol_B3_TC , \t\tSUM(LV_Bulk_B3)AS LV_Bulk_B3 , \t\tSUM(Med_Vol_B3)AS Med_Vol_B3 , \t\tSUM(High_Vol_B3) AS High_Vol_B3 , \t    (SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) + \t\tSUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)+ \t\tSUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT)+ \t\tSUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL )+ \t\tSUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)+ \t\tSUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) + \t\tSUM(Low_Vol_B3_Com)+ \t\tSUM(Low_Vol_B3_Ind)+ \t\tSUM(Low_Vol_B3_Agr)+ \t\tSUM(Low_Vol_B3_Ins)+ \t\tSUM(Low_Vol_B3_SL)+ \t\tSUM(Low_Vol_B3_PHA)+ \t\tSUM(Low_Vol_B3_TC)+ \t\tSUM(LV_Bulk_B3)+ \t\tSUM(Med_Vol_B3)+ \t\tSUM(High_Vol_B3)) AS Grand_Total \t\tFROM `t_bpc_energy_utilization_dzongkhag_wise2` a \t\tWHERE a.`Dzongkhag_Id`=? AND a.`Data_Month`=? AND a.`Data_Year`=?) t";
    private static final String GET_HYDROPLANT = "SELECT a.`Plant_Name`,DATE_FORMAT(a.`Record_Date`,'%d %M %Y') AS RecordDate, a.`Max_Inflow`,a.`Min_Inflow`,a.`Max_Frequency`,a.`Min_Frequency`FROM `t_hourly_data_dgpc1`a WHERE a.`Record_Date`=? AND a.`Plant_Id`=? LIMIT 1";
    private static final String GET_REPORT_ON_MINIHYDRO = "SELECT a.`Plant_Name`,a.`MU`,a.`MW`  FROM `t_monthly_mini_hydro` a WHERE a.`Month`=? AND a.`Year`=?";
    private static final String GET_REPORT_ON_HYDROPLANT = "SELECT a.`Unit_name`,a.`Record_hour`,a.`MW`,a.`MU`,a.`MVAR`,a.`PF`, a.`Remarks` FROM `t_hourly_data_dgpc2` a LEFT JOIN `t_hourly_data_dgpc1` b ON a.`PRecord_Id`=b.`Record_Id` WHERE b.`Record_Date`=? AND  b.`Plant_Id`=?";
    private static final String GET_REPORT_ON_hourlyconsumption = "SELECT a.`Record_hour`,a.`MW`,a.`MVAR`,ROUND((a.`MW` / (b.`capacity` / .9)),2)AS LF FROM `t_hourly_data_bpc` a LEFT JOIN `t_sub_station_master` b ON a.`Sub_Station_Id` = b.`Substation_Code` WHERE a.`Date_Of_Reading` =? AND b.`Substation_Code`=?";
    private static final String GET_REPORT_ON_Major_plantwise = "SELECT a.`Plant_Id`,a.`Plant_Name`,SUM(b.`MU`) AS MU FROM `t_hourly_data_dgpc1` a LEFT JOIN `t_hourly_data_dgpc2`b ON a.`Record_Id`=b.`PRecord_Id` WHERE a.`Record_Date` BETWEEN ? AND ? GROUP BY a.`Plant_Id`";
    private static final String GET_SUBSTATIONAME = "SELECT DATE_FORMAT(b.`Date_Of_Reading`,'%d %M %Y') AS recorddate,b.`Sub_Station_Name` FROM `t_hourly_data_bpc` b WHERE b.`Date_Of_Reading`=? AND b.`Sub_Station_Id`=? ";
    private static final String GET_REPORT_ON_WINDPOWERPLANT = "SELECT a.`Plant_Name`,a.`Day`,a.`T1_Energy_Generated`,a.`T2_Energy_Generated`,a.`Total_Energy_Generated`,a.`T1_Machine_Availability(hrs)`,a.`T2_Machine_Availability(hrs)` FROM `t_monthly_wind_power` a WHERE a.`Month`=? AND a.`Year`=?";
    private static final String GET_WINDPOWER = "SELECT a.`Month`, CASE a.`Month`WHEN '1' THEN 'January'WHEN '2' THEN 'February'WHEN '3' THEN 'March'WHEN '4' THEN 'April'WHEN '4' THEN 'May'WHEN '6' THEN 'June'WHEN '7' THEN 'July'WHEN '8' THEN 'August'WHEN '9' THEN 'September'WHEN '10' THEN 'October'WHEN '11' THEN 'November'WHEN '12' THEN 'December'END AS dmont,a.`Year` FROM `t_monthly_wind_power` a WHERE a.`Month`=? AND a.`Year`=?";
    private static final String GET_MINIHYDRO = "SELECT a.`Month`, CASE a.`Month`WHEN '1' THEN 'January'WHEN '2' THEN 'February'WHEN '3' THEN 'March'WHEN '4' THEN 'April'WHEN '4' THEN 'May'WHEN '6' THEN 'June'WHEN '7' THEN 'July'WHEN '8' THEN 'August'WHEN '9' THEN 'September'WHEN '10' THEN 'October'WHEN '11' THEN 'November'WHEN '12' THEN 'December'END AS dmont,a.`Year` FROM `t_monthly_mini_hydro` a WHERE a.`Month`=? AND a.`Year`=?";
    private static final String GET_REPORT_ON_Major_Transmission_Lines = "SELECT a.`Transmission_Name`, a.`400_kv_dc`,a.`400_kv_sc`,a.`220_kv_dc`,a.`220_kv_sc`,a.`132_kv_dc`,a.`132_kv_sc`,a.`66_kv_dc`,a.`66_kv_sc`,a.`66_kv_qc`,a.`UG`,a.`Remarks` FROM `t_trasmission_master`a ";
    private static final String GET_ERROR_DETAILS = "SELECT Error_Details FROM t_error_details WHERE Error_Code=?";
    private static final String GET_USER_LIST = "SELECT a.`User_Id`,b.`Role_Id`,d.`Role_Name`,a.`Name`,f.`Report_Id`, a.`Email_Address`,a.`Designation`,a.`Mobile_Number`, a.`Is_Active`, a.`Created_Date`,DATE_FORMAT(a.`Last_Login_Date`,'%d-%m-%Y') Last_Login_Date FROM `t_user_master` a LEFT JOIN `t_user_role_mapping` b ON a.`User_Id` = b.`User_Id` LEFT JOIN `t_user_location_mapping` c ON a.`User_Id` = c.`User_Id` LEFT JOIN `t_role_master` d ON b.`Role_Id` =d.`Role_Id` LEFT JOIN `t_user_report_mapping` e ON a.`User_Id` = e.`User_Id`LEFT JOIN `t_report_master` f ON e.`Report_Id` = f.`Report_Id`WHERE a.Logical_Delete <> 'Y' GROUP BY a.User_Id ORDER BY a.`Created_Date` DESC";
    private static final String INSERT_INTO_T_USER_MASTER = "INSERT INTO `t_user_master` (`User_Id`,             `Name`,             `Gender`,             `Designation`,             `Mobile_Number`,             `Email_Address`,             `Password`,             `Password_Salt`,             `Is_Active`,               `Location_Id`,              `Created_Date`) VALUES (?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP);";
    private static final String INSERT_INTO_USER_ROLE_MAPPING = "INSERT INTO `t_user_role_mapping` (`User_Id`, `Role_Id`) VALUES (?, ?)";
    private static final String DELETE_FROM_T_USER_REPORT_MAPPING = "DELETE FROM `t_user_report_mapping` WHERE `User_Id` = ?";
    private static final String INSERT_INTO_USER_REPORT_MAPPING = " INSERT INTO `t_user_report_mapping` (`User_Id`, `Report_Id`) VALUES (?, ?) ";
    private static final String GET_PUBLIC_MENU = " SELECT a.`Menu_Id`,a.`Menu_Name`,IF(a.`Is_Active`='Y','YES','NO') Is_Active FROM `t_menu_master` a WHERE a.`Menu_Cat_Type` = 'P' AND a.`Menu_Type` = 'P' AND a.`Is_Deleted` = 'N' ORDER BY a.`Parent_Menu_Sequence` ASC ";
    private static final String GET_TARIFF = " SELECT a.`Plant_Name`, a.`Tariff_Code`,a.`Tariff_Type`,a.`Tariff`, a.`Tariff_Set_Date`, IF(a.`Is_Active`='Y','YES','NO') `Is_Active` FROM `t_tariff_master` a WHERE a.`Delete_Status` ='N' ";
    private static final String GET_FEEDBACK_LIST = "SELECT a.FeedBack_Id,a.`Name`,a.`Address`,a.`Email_Id`,a.`FeedBack`,IF(a.`Is_Active`='Y','YES','NO') `Is_Active`  FROM `t_feedback_tbl`a WHERE a.`Delete_Status` ='N'";
    private static final String GET_FEEDBACKDETAILS = "SELECT a.`Name`,a.`Address`,a.`Email_Id`,a.`FeedBack` FROM `t_feedback_tbl`a  WHERE `FeedBack_Id` = ?";
    private static final String GET_WHEELING = " SELECT a.`Wheeling_Code`,a.`Wheeling`, a.`Wheeling_Set_Date`, IF(a.`Is_Active`='Y','YES','NO') `Is_Active` FROM `t_wheeling_master` a WHERE a.`Delete_Status`='N' ";
    private static final String GET_DG_PLANTS = " SELECT a.`Plant_Code`,a.`Plant_Name`,IF(a.`Is_Active`='Y','YES','NO') Is_Active FROM `t_dg_set_master` a WHERE a.`Delete_Status` = 'N'";
    private static final String GET_HYDROPOWER_PLANTS = " SELECT a.`Plant_Code`,a.`Plant_Name` ,IF(a.`Is_Active`='Y','YES','NO') `Is_Active` FROM `t_hydro_plant_master` a WHERE a.`Delete_Status`='N' ";
    private static final String GET_MINI_HYDROPOWER_PLANTS = " SELECT a.`Plant_Code`, a.`Plant_Name`, IF(a.`Is_Active`='Y','YES','NO') `Is_Active` FROM `t_mini_hydroplant_master` a WHERE a.`Delete_Status`='N' ";
    private static final String GET_WIND_HYDROPOWER_PLANTS = " SELECT a.`Plant_Code`, a.`Plant_Name`, IF(a.`Is_Active`='Y','YES','NO') `Is_Active` FROM `t_wind_plant_master` a WHERE a.`Delete_Status`='N' ";
    private static final String GET_SOLAR_HYDROPOWER_PLANTS = " SELECT a.`Plant_Code`, a.`Plant_Name`, IF(a.`Is_Active`='Y','YES','NO') `Is_Active` FROM `t_solar_plant_master` a WHERE a.`Delete_Status`='N' ";
    private static final String GET_TRANSMISSION = " SELECT a.`Transmission_Code`, a.`Transmission_Name`, IF(a.`Is_Active`='Y','YES','NO') `Is_Active` FROM `t_trasmission_master` a WHERE a.`Delete_Status`='N' ";
    private static final String GET_SUB_STATION = " SELECT a.`Substation_Code`, a.`Substation_Name`, IF(a.`Is_Active`='Y','YES','NO') `Is_Active` FROM `t_sub_station_master` a WHERE a.`Delete_Status`='N' ";
    private static final String GET_USER_DETAILS = " SELECT a.`User_Id`,a.`Gender`,b.`Role_Id`,e.`Report_Id`,d.`Role_Name`,a.`Name`, a.`Email_Address`,a.`Designation`,a.`Mobile_Number`,a.`Location_Id`, a.`Is_Active`, a.`Created_Date` FROM `t_user_master` a LEFT JOIN `t_user_role_mapping` b ON a.`User_Id` = b.`User_Id` LEFT JOIN `t_role_master` d ON b.`Role_Id` =d.`Role_Id` LEFT JOIN `t_user_report_mapping` e ON a.`User_Id` = e.`User_Id` LEFT JOIN `t_report_master` f ON e.`Report_Id` = f.`Report_Id` WHERE a.User_Id = ? GROUP BY a.User_Id";
    private static final String UPDATE_USER_DETAILS = " UPDATE `t_user_master` a SET a.`Name` = ?, a.`Gender` = ?,a.`Email_Address`= ?,a.`Mobile_Number` = ?, a.`Designation` = ?,a.`Location_Id` = ?  WHERE a.`User_Id` = ?";
    private static final String UPDATE_TARIFF_DETAILS = "UPDATE `t_tariff_master` SET `Plant_Name` =?, `Tariff` =? , `Tariff_Type` = ?, `Tariff_Set_Date` = ? WHERE `Tariff_Code` = ?;";
    private static final String UPDATE_WHEELING_DETAILS = " UPDATE `t_wheeling_master` SET  `Wheeling` = ?, `Wheeling_Set_Date` = ?  WHERE `Wheeling_Code` = ?";
    private static final String UPDATE_DG_PLANT_DETAILS = " UPDATE `t_dg_set_master` SET `Plant_Name` = ?, `Location` = ?,`Com_Operation_Date` = ?,`Installed_Capacity` = ?  WHERE `Plant_Code` = ? ";
    private static final String UPDATE_HYDRO_PLANT_DETAILS = " UPDATE `t_hydro_plant_master` SET `Plant_Name` = ?,  `Location` = ?, `Com_Operation_Date` = ?,  `DPR_Prepared_By` = ?,`DRP_Cost` = ?,`Project_Completion_Cost` = ?, `Installed_Capacity` = ?,  `Design_Energy` = ?, `Units_No` = ?, `Firm_Power` = ?, `Catchment_Area` = ?, `Net_Head` = ?,`Gross_Head` = ?,  `Voltage_Gen` = ?,`Voltage_Trans` = ?, `Switch_Yard` = ?, `Gen_Trans_Capacity` = ?, `No_Ckts` = ?, `No_Bays` = ?, `Switch_Yard_Type` = ?, `Discharge` = ?, `Turbine_Type` = ?,`Loan_Financing` = ?, `Grant_equity` = ?,`Tariff` = ? WHERE `Plant_Code` = ? ";
    private static final String UPDATE_MINIHYDRO_DETAILS = " UPDATE `t_mini_hydroplant_master` SET `Plant_Name` = ?,  `Location` = ?,  `Com_Operation_Date` = ?, `Installed_Capacity` = ?,  `Design_Energy` = ?,  `Units_No` =?,  `Gross_Head` = ?,  `Voltage_Generation` = ?,  `Voltage_Transmission` = ?,  `Gen_Trans_Capacity` = ?,  `No_Ckts` = ? WHERE `Plant_Code` = ? ";
    private static final String UPDATE_WINDPOWER_DETAILS = " UPDATE `t_wind_plant_master` SET `Plant_Name` = ?,  `Location` = ?, `Com_Operation_Date` = ?,  `Installed_Capacity` = ?,  `Design_Energy` = ? WHERE `Plant_Code` = ?";
    private static final String UPDATE_SOLARPOWER_DETAILS = " UPDATE `t_solar_plant_master` SET `Plant_Name` = ?, `Location` = ?, `Com_Operation_Date` = ?, `Installed_Capacity` = ?, `Design_Energy` = ? WHERE `Plant_Code` = ? ";
    private static final String UPDATE_TRANSMISSION_DETAILS = "UPDATE `t_trasmission_master` SET `Transmission_Name` = ?,`400_kv_dc` = ?,`400_kv_sc` = ?,`220_kv_dc` = ?,`220_kv_sc` = ?,`132_kv_dc` = ?,`132_kv_sc` = ?,`66_kv_dc` = ?,`66_kv_sc` = ?,`66_kv_qc` = ?,`UG` = ?,`Type_of_Conductor` = ?,`Remarks` = ?,WHERE `Transmission_Code` = ?";
    private static final String UPDATE_SUB_STATION_DETAILS = " UPDATE `t_sub_station_master` SET `Substation_Name` = ?, `Location` = ?, `Com_Operation_Date` = ?,`Capacity` = ?,`Area` = ? WHERE `Substation_Code` = ? ";
    private static final String DELETE_FROM_T_USER_ROLE_MAPPING = "DELETE FROM `t_user_role_mapping` WHERE `User_Id` = ?";
    private static final String UPDATE_T_USER_MASTER_WITH_LOGICAL_DELETE = "UPDATE t_user_master a SET a.`Logical_Delete` = ? WHERE a.`User_Id` = ?";
    private static final String UPDATE_T_USER_MASTER_WITH_ACTIVATION_FLAG = "UPDATE t_user_master a SET a.`Is_Active` = ? WHERE a.`User_Id` = ?";
    private static final String GET_LAST_MENU_ID = "SELECT a.`Menu_Id` FROM `t_menu_master` a ORDER  BY a.`Menu_Id` DESC LIMIT  1";
    private static final String INSERT_INTO_T_MENU_CONTENT = "INSERT INTO t_menu_content (`Menu_Id`,`Content`,`Display_Status`,`Created_Date`) VALUES (?,?,?,?)";
    private static final String GET_LAST_PARENT_MENU_SECQUENCE = "SELECT a.`Parent_Menu_Sequence` FROM `t_menu_master` a WHERE a.`Menu_Cat_Type` = 'P' ORDER  BY a.`Parent_Menu_Sequence` DESC LIMIT  1";
    private static final String INSERT_PORTAL_MENU = "INSERT INTO `t_menu_master`(`Menu_Id`,`Menu_Cat_Type`,`Parent_Menu_Id`,`Menu_Name`,`Parent_Menu_Sequence`,Menu_Sequence_No,`Menu_Type`,`Is_Active`) VALUES (?,?,?,?,?,?,?,?);";
    private static final String INSERT_INTO_T_TARIFF = " INSERT INTO `t_tariff_master`(`Plant_Name`,`Tariff`, `Tariff_Type`, `Tariff_Set_Date`,`Is_Active`)VALUES (?,?,?,?,?) ";
    private static final String INSERT_INTO_T_WHEELING = " INSERT INTO `t_wheeling_master` (`Wheeling`,`Wheeling_Set_Date`,`Is_Active`)VALUES (?,?,?) ";
    private static final String INSERT_INTO_T_DG = " INSERT INTO `t_dg_set_master` (`Plant_Name`,`Location`,`Installed_Capacity`,`Com_Operation_Date`,`Is_Active`)VALUES (?,?,?,?,?) ";
    private static final String INSERT_INTO_T_HYDROPOWER = " INSERT INTO `t_hydro_plant_master`(`Plant_Name`,`Location`,`Com_Operation_Date`,`DPR_Prepared_By`,`DRP_Cost`,`Project_Completion_Cost`,`Installed_Capacity`,`Design_Energy`,`Units_No`,`Firm_Power`,`Catchment_Area`,`Net_Head`,`Gross_Head`,`Voltage_Gen`,`Voltage_Trans`,`Switch_Yard`,`Gen_Trans_Capacity`,`No_Ckts`,`No_Bays`,`Switch_Yard_Type`,`Discharge`,`Turbine_Type`,`Loan_Financing`,`Grant_equity`,`Tariff`,`Is_Active`) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ";
    private static final String INSERT_INTO_T_MINI_HYDROPOWER = " INSERT INTO `t_mini_hydroplant_master`(`Plant_Name`,`Location`,`Com_Operation_Date`,`Installed_Capacity`,`Design_Energy`,`Units_No`,`Gross_Head`,`Voltage_Generation`,`Voltage_Transmission`,`Gen_Trans_Capacity`,`No_Ckts`,`Is_Active`)VALUES (?,?,?,?,?,?,?,?,?,?,?,?); ";
    private static final String INSERT_INTO_T_WINDPOWER = " INSERT INTO `t_wind_plant_master`(`Plant_Name`,`Location`,`Com_Operation_Date`,`Installed_Capacity`,`Design_Energy`,`Is_Active`)VALUES (?,?,?,?,?,?) ";
    private static final String INSERT_INTO_T_SOLARPOWER = " INSERT INTO `t_solar_plant_master`(`Plant_Name`,`Location`,`Com_Operation_Date`,`Installed_Capacity`,`Design_Energy`,`Is_Active`)VALUES (?,?,?,?,?,?) ";
    private static final String INSERT_INTO_T_TRANSMISSION = " INSERT INTO `t_trasmission_master`(`Transmission_Name`,`400_kv_dc`,`400_kv_sc`,`220_kv_dc`,`220_kv_sc`,`132_kv_dc`,`132_kv_sc`,`66_kv_dc`,`66_kv_sc`,`66_kv_qc`,`UG`,`Type_of_Conductor`,`Remarks`,`Is_Active`)VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?) ";
    private static final String INSERT_INTO_T_SUB_STATION = " INSERT INTO `t_sub_station_master`(`Substation_Name`,`Location`,`Com_Operation_Date`,`Capacity`,`Transformer`,`Voltage_Ratio`,`Area`,`Is_Active`)VALUES (?,?,?,?,?,?,?,?) ";
    private static final String GET_LAST_CHILD_MENU_SECQUENCE = "SELECT a.`Menu_Sequence_No` FROM `t_menu_master` a WHERE a.`Menu_Type`= 'S' AND a.`Parent_Menu_Id` = ? ORDER  BY a.`Menu_Sequence_No` DESC LIMIT  1";
    private static final String GET_CHILD_MENT = "SELECT a.`Menu_Id`,a.`Menu_Name`,IF(a.`Is_Active`='Y','YES','NO') Is_Active,a.`Parent_Menu_Id` FROM `t_menu_master` a WHERE a.`Parent_Menu_Id` =? AND a.`Menu_Type` ='S' AND a.`Is_Deleted` = 'N' ORDER BY a.`Menu_Sequence_No` ASC";
    private static final String UPDATE_MENU_MASTER_ACTIVATION_FALG = "UPDATE `t_menu_master` a SET a.`Is_Active` = ? WHERE a.`Menu_Id` = ?";
    private static final String UPDATE_ON_DELETE_PUBLIC_MENU = "UPDATE `t_menu_master` a SET a.`Is_Active` = ? ,a.`Is_Deleted` = ? WHERE a.`Menu_Id` = ?";
    private static final String UPDATE_T_ANNOUNCEMENT_DTLS = "UPDATE t_announcement_dtls SET announcement_title=?,announcement_content=? WHERE announcement_id=?";
    private static final String UPDATE_T_MENU_DTLS = "UPDATE t_menu_master a LEFT JOIN t_menu_content b ON a.menu_id=b.menu_id SET a.menu_name=?,b.content=? WHERE a.menu_id=?";
    private static final String GET_TARIFF_DTLS = " SELECT  a.`Plant_Name`, a.`Tariff`, a.`Tariff_Type`, DATE_FORMAT(a.`Tariff_Set_Date`,'%d/%m/%Y') tariffSetDate, a.`Tariff_Code` FROM `t_tariff_master` a WHERE a.`Tariff_Code` = ?";
    private static final String GET_WHEELING_DTLS = " SELECT a.`Wheeling`, DATE_FORMAT(a.`Wheeling_Set_Date`,'%d/%m/%Y') WheelingSetDate, a.`Wheeling_Code` FROM `t_wheeling_master` a WHERE a.`Wheeling_Code` = ?";
    private static final String GET_DG_PLANT_DTLS = " SELECT  `Plant_Name`, `Location`, DATE_FORMAT(a.`Com_Operation_Date`,'%d/%m/%Y') Com_Operation_Date, `Installed_Capacity`, a.`Plant_Code` FROM `t_dg_set_master` a WHERE a.`Plant_Code` = ?";
    private static final String GET_HYDROPOWER_PLANT_DTLS = " SELECT  `Plant_Name`, `Location`, DATE_FORMAT(`Com_Operation_Date`,'%d/%m/%Y') Com_Operation_Date, `DPR_Prepared_By`, `DRP_Cost`, `Project_Completion_Cost`, `Installed_Capacity`, `Design_Energy`, `Units_No`, `Firm_Power`, `Catchment_Area`, `Net_Head`, `Gross_Head`, `Voltage_Gen`, `Voltage_Trans`, `Switch_Yard`, `Gen_Trans_Capacity`, `No_Ckts`, `No_Bays`, `Switch_Yard_Type`, `Discharge`, `Turbine_Type`, `Loan_Financing`, `Grant_equity`, `Tariff`, a.`Plant_Code` FROM `t_hydro_plant_master` a  WHERE a.`Plant_Code` = ?  ";
    private static final String GET_MINIHYDRO_PLANT_DTLS = " SELECT   `Plant_Name`, `Location`, DATE_FORMAT(`Com_Operation_Date`,'%d/%m/%Y') Com_Operation_Date, `Installed_Capacity`, `Design_Energy`, `Units_No`, `Gross_Head`, `Voltage_Generation`, `Voltage_Transmission`, `Gen_Trans_Capacity`, `No_Ckts`, a.`Plant_Code` FROM `t_mini_hydroplant_master` a WHERE a.`Plant_Code` = ? ";
    private static final String GET_WINDPOWER_PLANT_DTLS = " SELECT  `Plant_Name`, `Location`, DATE_FORMAT(`Com_Operation_Date`,'%d/%m/%Y') Com_Operation_Date, `Installed_Capacity`, `Design_Energy`, `Plant_Code`  FROM `t_wind_plant_master` a WHERE a.`Plant_Code` = ? ";
    private static final String GET_SOLARPOWER_PLANT_DTLS = " SELECT  `Plant_Name`, `Location`, DATE_FORMAT(`Com_Operation_Date`,'%d/%m/%Y') Com_Operation_Date, `Installed_Capacity`, `Design_Energy`, `Plant_Code` FROM `t_solar_plant_master` a WHERE a.`Plant_Code` = ? ";
    private static final String GET_TRANSMISSION_DTLS = " SELECT  `Transmission_Name`, `400_kv_dc`, `400_kv_sc`, `220_kv_dc`, `220_kv_sc`, `132_kv_dc`, `132_kv_sc`, `66_kv_dc`, `66_kv_sc`, `66_kv_qc`, `UG`, `Type_of_Conductor`, `Remarks`, `Transmission_Code` FROM  `t_trasmission_master` a WHERE a.`Transmission_Code` = ? ";
    private static final String GET_SUB_STATION_DTLS = " SELECT  `Substation_Name`, `Location`, DATE_FORMAT(`Com_Operation_Date`,'%d/%m/%Y') Com_Operation_Date, `Capacity`, `Voltage_Ratio`, `Transformer`,  `Area`, `Substation_Code` FROM `t_sub_station_master` a WHERE a.`Substation_Code` = ? ";
    private static final String GET_MENU_DTLS = "SELECT a.`Menu_Name` title,b.`Content` FROM `t_menu_master` a LEFT JOIN `t_menu_content` b ON a.`Menu_Id`=b.`Menu_Id` WHERE a.Menu_Id=? AND a.`Menu_Cat_Type`=?";
    private static final String INSERT_FEEDBACK = "INSERT INTO `t_feedback_tbl`(`Name`,`Address`,`Email_Id`,`FeedBack`) VALUE(?,?,?,?);";
    private static final String GET_TOTL_INSTAL_CAPICITY = " SELECT  'Major Hydropower Plants' NAME,  SUM(Installed_Capacity) Y,  'Major' drilldown  FROM  t_hydro_plant_master  UNION  SELECT  'Mini Hydropower Plants' NAME,  SUM(Installed_Capacity / 1000) Y,  'Mini' drilldown  FROM  t_mini_hydroplant_master  UNION  SELECT  'Solar Power Plants' NAME,  SUM(Installed_Capacity / 1000) Y,  'Wind' drilldown  FROM  t_wind_plant_master  UNION  SELECT  'Wind Power Plants' NAME,  SUM(Installed_Capacity / 1000) Y,  'Solar' drilldown  FROM  t_solar_plant_master  UNION  SELECT  'Diesel Generation Plants' NAME,  SUM(Installed_Capacity / 1000) Y,  'Diesel' drilldown  FROM  t_dg_set_master";
    private static final String GET_TOTAL_INSTAL_CAPICITY = "SELECT 'Major Hydro Power Plants  - ' plantName, SUM(Installed_Capacity)  totalCapacity FROM t_hydro_plant_master UNION SELECT 'Mini Hydro Power Plants - ' plantName, SUM(Installed_Capacity/1000) totalCapacity FROM t_mini_hydroplant_master UNION SELECT 'Solar Power Plants - ' plantName, SUM(Installed_Capacity/1000)totalCapacity FROM t_solar_plant_master UNION SELECT 'Wind Power Plants - ' plantName, SUM(Installed_Capacity/1000) totalCapacity FROM t_wind_plant_master UNION SELECT 'DG Power Plants - ' plantName, SUM(Installed_Capacity/1000) totalCapacity FROM t_dg_set_master";
    private static final String GET_TOTAL_GENERATION_MU = "SELECT  IF( (FORMAT(SUM(a.`MU`), 2)) IS NULL,  'Empty', FORMAT(SUM(a.`MU`), 2)  ) AS TOTAL_MU  FROM  `t_hourly_data_dgpc2` a  WHERE a.`Record_Date` BETWEEN ? AND ?";
    private static final String GET_TOTAL_DEMAND = "SELECT Record_hour, SUM(MW) AS peakMW FROM t_hourly_data_bpc WHERE Date_Of_Reading = ? GROUP BY Record_hour HAVING SUM(MW) = (SELECT MAX(peakMW) FROM (SELECT SUM(MW)  peakMW, Record_hour FROM t_hourly_data_bpc WHERE Date_Of_Reading = ? GROUP BY Record_hour) tab)";
    private static final String UPDATE_TARIFF_MASTER_ACTIVATION_FALG = " UPDATE `t_tariff_master` a SET a.`Is_Active` = ? WHERE a.`Tariff_Code` = ? ";
    private static final String UPDATE_ON_DELETE_TARIFF = " UPDATE `t_tariff_master` a SET a.`Is_Active` = ? ,a.`Delete_Status` = ? WHERE a.`Tariff_Code` = ? ";
    private static final String UPDATE_ON_DELETE_FEEDBACK = "UPDATE `t_feedback_tbl` a SET a.`Is_Active` = ?, a.`Delete_Status` = ? WHERE a.`FeedBack_Id`= ?";
    private static final String UPDATE_DG_MASTER_ACTIVATION_FALG = " UPDATE `t_dg_set_master` a SET a.`Is_Active` = ? WHERE a.`Plant_Code` = ? ";
    private static final String UPDATE_ON_DELETE_DG = " UPDATE `t_dg_set_master` a SET a.`Is_Active` = ? ,a.`Delete_Status` = ? WHERE a.`Plant_Code` = ?";
    private static final String UPDATE_WHEELING_MASTER_ACTIVATION_FALG = " UPDATE `t_wheeling_master` a SET a.`Is_Active` = ? WHERE a.`Wheeling_Code` = ? ";
    private static final String UPDATE_ON_DELETE_WHEELING = " UPDATE `t_wheeling_master` a SET a.`Is_Active` = ? ,a.`Delete_Status` = ? WHERE a.`Wheeling_Code` = ? ";
    private static final String UPDATE_HYDROPOWER_MASTER_ACTIVATION_FALG = " UPDATE `t_hydro_plant_master` a SET a.`Is_Active` = ? WHERE a.`Plant_Code` = ? ";
    private static final String UPDATE_ON_DELETE_HYDROPOWER = " UPDATE `t_hydro_plant_master` a SET a.`Is_Active` = ? ,a.`Delete_Status` = ? WHERE a.`Plant_Code` = ? ";
    private static final String UPDATE_MINIHYDROPOWER_MASTER_ACTIVATION_FALG = " UPDATE `t_mini_hydroplant_master` a SET a.`Is_Active` = ? WHERE a.`Plant_Code` = ? ";
    private static final String UPDATE_ON_DELETE_MINIHYDROPOWER = " UPDATE `t_mini_hydroplant_master` a SET a.`Is_Active` = ? ,a.`Delete_Status` = ? WHERE a.`Plant_Code` = ? ";
    private static final String UPDATE_WINDPOWER_MASTER_ACTIVATION_FALG = " UPDATE `t_wind_plant_master` a SET a.`Is_Active` = ? WHERE a.`Plant_Code` = ? ";
    private static final String UPDATE_ON_DELETE_WINDPOWER = " UPDATE `t_wind_plant_master` a SET a.`Is_Active` = ? ,a.`Delete_Status` = ? WHERE a.`Plant_Code` = ? ";
    private static final String UPDATE_SOLARPOWER_MASTER_ACTIVATION_FALG = " UPDATE `t_solar_plant_master` a SET a.`Is_Active` = ? WHERE a.`Plant_Code` = ? ";
    private static final String UPDATE_ON_DELETE_SOLARPOWER = " UPDATE `t_solar_plant_master` a SET a.`Is_Active` = ? ,a.`Delete_Status` = ? WHERE a.`Plant_Code` = ? ";
    private static final String UPDATE_TRANSMISSION_MASTER_ACTIVATION_FALG = " UPDATE `t_trasmission_master` a SET a.`Is_Active` = ? WHERE a.`Transmission_Code` = ? ";
    private static final String UPDATE_ON_DELETE_TRANSMISSION = " UPDATE `t_trasmission_master` a SET a.`Is_Active` = ? ,a.`Delete_Status` = ? WHERE a.`Transmission_Code` = ? ";
    private static final String UPDATE_SUB_STATION_MASTER_ACTIVATION_FALG = " UPDATE `t_sub_station_master` a SET a.`Is_Active` = ? WHERE a.`Substation_Code` = ? ";
    private static final String UPDATE_ON_DELETE_SUB_STATION = " UPDATE `t_sub_station_master` a SET a.`Is_Active` = ? ,a.`Delete_Status` = ? WHERE a.`Substation_Code` = ? ";
    private static String GET_HYDROPOWER_INSATLLED_CAPACITY;
    private static String GET_MINIHYDRO_INSATLLED_CAPACITY;
    private static String GET_WINDPOWER_INSATLLED_CAPACITY;
    private static String GET_SOLARPOWER_INSATLLED_CAPACITY;
    private static String GET_DG_PLANT_INSATLLED_CAPACITY;
    private static String GET_TOTAL_GENERATION_MU_PLANT_WISE;
    private static String GET_TOTAL_DEMAND_SUB_STATION_WISE;
    private static final String GET_DATABASE_CONFIG_DTLS = "SELECT `Mysql_Path`,`Database_Name`,`Database_User_Name`,`Database_Password`,`Database_Host`,`Backup_Path` FROM `t_database_config_master`";
    private static final String UPDATE_T_DATABASE_CONFIG_MASTER = " UPDATE  `t_database_config_master`  SET  `Mysql_Path` = ?,  `Database_Name` = ?,  `Database_User_Name` = ?,  `Database_Password` = ?,  `Database_Host` = ?,  `Backup_Path` = ?";
    private static final String UPDATE_ON_DELETE_NOTIFICATION = "UPDATE `t_user_notification_mapping` a SET a.`Is_Deleted` = 'Y' WHERE a.`User_notify_id` = ?";
    private static final String UPDATE_ON_COMPOSE_DELETE = "UPDATE `t_notification_details` a SET a.`Is_Deleted` = 'Y' WHERE a.`Notification_Id` = ?";
    private static final String INSERT_INTO_NOTIFICATION_TS = "INSERT INTO `t_notification_details`(`Notification_Title`,`Notification`,`Created_By`,`Created_Date`) VALUES (?,?,?,CURRENT_TIMESTAMP);";
    private static final String INSERT_INTO_NOTIFICATION_MS = "INSERT INTO `t_notification_details`(`Notification_Title`,`Notification`,`Location_Type`,`Location_Id`,`Created_By`,`Created_Date`) VALUES (?,?,?,?,?,CURRENT_TIMESTAMP);";
    private static final String GET_NOTIFICATION_ID = "SELECT a.`Notification_Id` FROM `t_notification_details` a ORDER BY  a.`Notification_Id` DESC LIMIT 1";
    private static final String GET_TO_BPC_MAN_USERS = "SELECT a.`User_Id` FROM `t_user_master` a LEFT JOIN `t_user_role_mapping` b ON a.`User_Id` = b.`User_Id` WHERE b.`Role_Id` ='4' AND a.`Is_Active` ='Y'";
    private static final String GET_TO_SUB_STATION_USERS = "SELECT a.`User_Id` FROM `t_user_master` a LEFT JOIN `t_user_role_mapping` b ON a.`User_Id` = b.`User_Id` LEFT JOIN `t_sub_station_master` c ON a.`Location_Id` = c.`Substation_Code` WHERE b.`Role_Id` ='3' AND c.`Substation_Code` = ? AND a.`Is_Active` ='Y';";
    private static final String GET_TO_ALL_USERS = "SELECT b.`User_Id` FROM `t_user_role_mapping` b WHERE b.`Role_Id` IN ('3','4') AND b.`User_Id` IN (SELECT User_Id FROM `t_user_master` WHERE `Is_Active`= 'Y')";
    private static final String INSERT_INTO_NOTIFY_USER_MAPPING = "INSERT INTO `t_user_notification_mapping` (`Notification_Id`,`User_Id`) VALUES (?,?);";
    private static final String GET_ALL_USER_FOR_PARTICULAR_LOC = "SELECT a.`User_Id` FROM `t_user_master` a LEFT JOIN `t_user_role_mapping` b ON a.`User_Id` = b.`User_Id` WHERE b.`Role_Id` ='3' AND a.`Is_Active` ='Y'";
    private static final String HOST_ADDRESS = "HOST_ADDRESS";
    private static final String SMTP_PORT = "SMTP_PORT";
    private static final String DEBUG_FLAG = "DEBUG_FLAG";
    private static final String STARTTLS_FLAG = "STARTTLS_ENABLE_FLAG";
    private static final String FROM_ADDRESS = "FROM_ADDRESS";
    private static final String USER_ADDRESS = "MAIL_USER_ADDRESS";
    private static final String USER_PASSWORD = "MAIL_USER_PASSWORD";
    private static final String SMTP_AUTH = "SMTP_AUTH_FLAG";
    private static final String UPDATE_T_EMAIL_CONFIG_MASTER = " UPDATE  `t_email_config_master`  SET  `Configuration` = ?  WHERE Config_Type = ?";
    private static final String UPDATE_USER_PASSWORD = "UPDATE t_user_master a SET a.`Password_Salt`=?,a.`Password`=? WHERE a.`User_Id` = ?";
    
    static {
        AdminDAO.date = new Date(System.currentTimeMillis());
        AdminDAO.GET_HYDROPOWER_INSATLLED_CAPACITY = " SELECT a.`Plant_Name`, a.`Installed_Capacity`, DATE_FORMAT(a.`Com_Operation_Date`,'%d-%m-%Y') AS COD FROM `t_hydro_plant_master` a WHERE a.`Delete_Status` = 'N' AND a.`Is_Active` = 'Y' ";
        AdminDAO.GET_MINIHYDRO_INSATLLED_CAPACITY = " SELECT a.`Plant_Name`, a.`Installed_Capacity` FROM `t_mini_hydroplant_master` a WHERE a.`Delete_Status` = 'N' AND a.`Is_Active` = 'Y' ";
        AdminDAO.GET_WINDPOWER_INSATLLED_CAPACITY = " SELECT a.`Plant_Name`, a.`Installed_Capacity` FROM `t_wind_plant_master` a WHERE a.`Delete_Status` = 'N' AND a.`Is_Active` = 'Y' ";
        AdminDAO.GET_SOLARPOWER_INSATLLED_CAPACITY = " SELECT a.`Plant_Name`, a.`Installed_Capacity` FROM `t_solar_plant_master` a WHERE a.`Delete_Status` = 'N' AND a.`Is_Active` = 'Y' ";
        AdminDAO.GET_DG_PLANT_INSATLLED_CAPACITY = " SELECT a.`Plant_Name`, a.`Installed_Capacity` FROM `t_dg_set_master` a WHERE a.`Delete_Status` = 'N' AND a.`Is_Active` = 'Y' ";
        AdminDAO.GET_TOTAL_GENERATION_MU_PLANT_WISE = " SELECT  a.`Plant_Name`, IF((FORMAT(SUM(a.`MU`), 2)) IS NULL,  'Empty', FORMAT(SUM(a.`MU`), 2) ) AS TOTAL_MU FROM   `t_hourly_data_dgpc2` a WHERE a.`Record_Date` = ? GROUP BY a.`Plant_Name` ";
        AdminDAO.GET_TOTAL_DEMAND_SUB_STATION_WISE = " SELECT  a.Sub_Station_Name, IF( a.`MW` IS NULL, 'Empty', FORMAT(MAX(a.`MW`), 2) ) AS Higest_MW FROM `t_hourly_data_bpc` a WHERE a.Date_Of_Reading = ? GROUP BY a.Sub_Station_Name ";
    }
    
    public static AdminDAO getInstance() {
        if (AdminDAO.adminDAO == null) {
            AdminDAO.adminDAO = new AdminDAO();
        }
        return AdminDAO.adminDAO;
    }
    
    public List<UserDTO> getUserList() throws HPSException, HPSSystemException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        final List<UserDTO> userList = new ArrayList<UserDTO>();
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement("SELECT a.`User_Id`,b.`Role_Id`,d.`Role_Name`,a.`Name`,f.`Report_Id`, a.`Email_Address`,a.`Designation`,a.`Mobile_Number`, a.`Is_Active`, a.`Created_Date`,DATE_FORMAT(a.`Last_Login_Date`,'%d-%m-%Y') Last_Login_Date FROM `t_user_master` a LEFT JOIN `t_user_role_mapping` b ON a.`User_Id` = b.`User_Id` LEFT JOIN `t_user_location_mapping` c ON a.`User_Id` = c.`User_Id` LEFT JOIN `t_role_master` d ON b.`Role_Id` =d.`Role_Id` LEFT JOIN `t_user_report_mapping` e ON a.`User_Id` = e.`User_Id`LEFT JOIN `t_report_master` f ON e.`Report_Id` = f.`Report_Id`WHERE a.Logical_Delete <> 'Y' GROUP BY a.User_Id ORDER BY a.`Created_Date` DESC");
                rs = pst.executeQuery();
                while (rs.next()) {
                    final UserDTO dto = new UserDTO();
                    dto.setUserId(rs.getString("User_Id"));
                    dto.setName(rs.getString("Name"));
                    dto.setMobileNumber(rs.getString("Mobile_Number"));
                    dto.setEmailAddress(rs.getString("Email_Address"));
                    dto.setRoleName(rs.getString("Role_Name"));
                    dto.setDesignation(rs.getString("Designation"));
                    dto.setRoleId(rs.getString("Role_Id"));
                    dto.setIsActive(rs.getString("Is_Active"));
                    dto.setLastLogin(rs.getString("Last_Login_Date"));
                    userList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException("###Error at AdminDAO[getUserList]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return userList;
    }
    
    public String SumbitDetails(final AdminDTO dtlDto) throws Exception {
        Connection conn = null;
        PreparedStatement pst = null;
        final ResultSet rs = null;
        final int count = 0;
        String query = null;
        String result = "Error";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            query = "INSERT INTO `t_feedback_tbl`(`Name`,`Address`,`Email_Id`,`FeedBack`) VALUE(?,?,?,?);";
            pst = conn.prepareStatement(query);
            pst.setString(1, dtlDto.getName());
            pst.setString(2, dtlDto.getAddress());
            pst.setString(3, dtlDto.getEmailId());
            pst.setString(4, dtlDto.getFeedback());
            pst.executeUpdate();
            conn.commit();
            result = "Success";
        }
        catch (SQLException e) {
            conn.rollback();
            e.printStackTrace();
            System.out.println("Error Occure at DetailSubmitDAO.SumbitDetails() " + e.fillInStackTrace());
            return result;
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return result;
    }
    
    public String addUser(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        PreparedStatement pst2 = null;
        PreparedStatement pst3 = null;
        String result = "ADD_USER_FAILURE";
        try {
            final String salt = PasswordEncryptionUtil.generateSalt(512).get();
            final String hashPassword = PasswordEncryptionUtil.hashPassword(dto.getPassword(), salt).get();
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            if (conn != null) {
                pst = conn.prepareStatement("INSERT INTO `t_user_master` (`User_Id`,             `Name`,             `Gender`,             `Designation`,             `Mobile_Number`,             `Email_Address`,             `Password`,             `Password_Salt`,             `Is_Active`,               `Location_Id`,              `Created_Date`) VALUES (?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP);");
                pst.setString(1, dto.getEmailId());
                pst.setString(2, dto.getName());
                pst.setString(3, dto.getGender());
                pst.setString(4, dto.getDesignation());
                pst.setString(5, dto.getMobileNumber());
                pst.setString(6, dto.getEmailId());
                pst.setString(7, hashPassword);
                pst.setString(8, salt);
                pst.setString(9, "Y");
                if (dto.getRoleId().equalsIgnoreCase("3")) {
                    pst.setString(10, dto.getSubstationId());
                }
                else {
                    pst.setString(10, null);
                }
                int count = pst.executeUpdate();
                if (count > 0) {
                    pst2 = conn.prepareStatement("INSERT INTO `t_user_role_mapping` (`User_Id`, `Role_Id`) VALUES (?, ?)");
                    pst2.setString(1, dto.getEmailId());
                    pst2.setString(2, dto.getRoleId());
                    count = pst2.executeUpdate();
                }
                if (count > 0) {
                    for (int i = 0; i < dto.getReportList().length; ++i) {
                        pst3 = conn.prepareStatement(" INSERT INTO `t_user_report_mapping` (`User_Id`, `Report_Id`) VALUES (?, ?) ");
                        pst3.setString(1, dto.getEmailId());
                        pst3.setString(2, dto.getReportList()[i]);
                        count = pst3.executeUpdate();
                    }
                    if (count > 0) {
                        result = "ADD_USER_SUCCESS";
                        conn.commit();
                    }
                }
            }
        }
        catch (Exception e) {
            conn.rollback();
            result = "ADD_USER_FAILURE";
            throw new HPSException("###Error at AdminDAO[addUser]: exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, (ResultSet)null, pst);
        }
        ConnectionManager.close(conn, (ResultSet)null, pst);
        return result;
    }
    
    public List<MenuVO> getPublicMenuList() throws HPSException, HPSSystemException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        final List<MenuVO> menuList = new ArrayList<MenuVO>();
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT a.`Menu_Id`,a.`Menu_Name`,IF(a.`Is_Active`='Y','YES','NO') Is_Active FROM `t_menu_master` a WHERE a.`Menu_Cat_Type` = 'P' AND a.`Menu_Type` = 'P' AND a.`Is_Deleted` = 'N' ORDER BY a.`Parent_Menu_Sequence` ASC ");
                rs = pst.executeQuery();
                while (rs.next()) {
                    final MenuVO dto = new MenuVO();
                    dto.setMenuId(rs.getString("Menu_Id"));
                    dto.setMenuName(rs.getString("Menu_Name"));
                    dto.setIsActive(rs.getString("Is_Active"));
                    menuList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException("###Error at AdminDAO[getPublicMenuList]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return menuList;
    }
    
    public List<MasterVO> gettariffList() throws HPSException, HPSSystemException {
        Connection conn = null;
        ResultSet rs = null;
        final List<MasterVO> tariffList = new ArrayList<MasterVO>();
        PreparedStatement pst = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT a.`Plant_Name`, a.`Tariff_Code`,a.`Tariff_Type`,a.`Tariff`, a.`Tariff_Set_Date`, IF(a.`Is_Active`='Y','YES','NO') `Is_Active` FROM `t_tariff_master` a WHERE a.`Delete_Status` ='N' ");
                rs = pst.executeQuery();
                while (rs.next()) {
                    final MasterVO dto = new MasterVO();
                    dto.setPlantname(rs.getString("Plant_Name"));
                    dto.setTariffCode(rs.getString("Tariff_Code"));
                    dto.setTariff(rs.getString("Tariff"));
                    dto.setTariffDate(rs.getString("Tariff_Set_Date"));
                    dto.setTariffType(rs.getString("Tariff_Type"));
                    dto.setIsActive(rs.getString("Is_Active"));
                    tariffList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException("###Error at AdminDAO[gettariffList]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return tariffList;
    }
    
    public List<MasterVO> getwheelingList() throws HPSException, HPSSystemException {
        Connection conn = null;
        ResultSet rs = null;
        final List<MasterVO> wheelingList = new ArrayList<MasterVO>();
        PreparedStatement pst = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT a.`Wheeling_Code`,a.`Wheeling`, a.`Wheeling_Set_Date`, IF(a.`Is_Active`='Y','YES','NO') `Is_Active` FROM `t_wheeling_master` a WHERE a.`Delete_Status`='N' ");
                rs = pst.executeQuery();
                while (rs.next()) {
                    final MasterVO dto = new MasterVO();
                    dto.setWheelingCode(rs.getString("Wheeling_Code"));
                    dto.setWheeling(rs.getString("Wheeling"));
                    dto.setWheelingDate(rs.getString("Wheeling_Set_Date"));
                    dto.setIsActive(rs.getString("Is_Active"));
                    wheelingList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException("###Error at AdminDAO[getwheelingList]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return wheelingList;
    }
    
    public List<MasterVO> getdgList() throws HPSException, HPSSystemException {
        Connection conn = null;
        ResultSet rs = null;
        final List<MasterVO> dgList = new ArrayList<MasterVO>();
        PreparedStatement pst = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT a.`Plant_Code`,a.`Plant_Name`,IF(a.`Is_Active`='Y','YES','NO') Is_Active FROM `t_dg_set_master` a WHERE a.`Delete_Status` = 'N'");
                rs = pst.executeQuery();
                while (rs.next()) {
                    final MasterVO dto = new MasterVO();
                    dto.setPlantCode(rs.getString("Plant_Code"));
                    dto.setPlantname(rs.getString("Plant_Name"));
                    dto.setIsActive(rs.getString("Is_Active"));
                    dgList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException("###Error at AdminDAO[getdgListList]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return dgList;
    }
    
    public List<MasterVO> gethydropowerList() throws HPSException, HPSSystemException {
        Connection conn = null;
        ResultSet rs = null;
        final List<MasterVO> hydropowerList = new ArrayList<MasterVO>();
        PreparedStatement pst = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT a.`Plant_Code`,a.`Plant_Name` ,IF(a.`Is_Active`='Y','YES','NO') `Is_Active` FROM `t_hydro_plant_master` a WHERE a.`Delete_Status`='N' ");
                rs = pst.executeQuery();
                while (rs.next()) {
                    final MasterVO dto = new MasterVO();
                    dto.setPlantCode(rs.getString("Plant_Code"));
                    dto.setPlantname(rs.getString("Plant_Name"));
                    dto.setIsActive(rs.getString("Is_Active"));
                    hydropowerList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException("###Error at AdminDAO[gethydropowerList]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return hydropowerList;
    }
    
    public List<MasterVO> getminihydropowerList() throws HPSException, HPSSystemException {
        Connection conn = null;
        ResultSet rs = null;
        final List<MasterVO> minihydropowerList = new ArrayList<MasterVO>();
        PreparedStatement pst = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT a.`Plant_Code`, a.`Plant_Name`, IF(a.`Is_Active`='Y','YES','NO') `Is_Active` FROM `t_mini_hydroplant_master` a WHERE a.`Delete_Status`='N' ");
                rs = pst.executeQuery();
                while (rs.next()) {
                    final MasterVO dto = new MasterVO();
                    dto.setPlantCode(rs.getString("Plant_Code"));
                    dto.setPlantname(rs.getString("Plant_Name"));
                    dto.setIsActive(rs.getString("Is_Active"));
                    minihydropowerList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException("###Error at AdminDAO[getminihydropowerList]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return minihydropowerList;
    }
    
    public List<MasterVO> getwindpwoerList() throws HPSException, HPSSystemException {
        Connection conn = null;
        ResultSet rs = null;
        final List<MasterVO> windpowerList = new ArrayList<MasterVO>();
        PreparedStatement pst = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT a.`Plant_Code`, a.`Plant_Name`, IF(a.`Is_Active`='Y','YES','NO') `Is_Active` FROM `t_wind_plant_master` a WHERE a.`Delete_Status`='N' ");
                rs = pst.executeQuery();
                while (rs.next()) {
                    final MasterVO dto = new MasterVO();
                    dto.setPlantCode(rs.getString("Plant_Code"));
                    dto.setPlantname(rs.getString("Plant_Name"));
                    dto.setIsActive(rs.getString("Is_Active"));
                    windpowerList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException("###Error at AdminDAO[getwindpwoerList]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return windpowerList;
    }
    
    public List<MasterVO> getsolarpwoerList() throws HPSException, HPSSystemException {
        Connection conn = null;
        ResultSet rs = null;
        final List<MasterVO> solarpowerList = new ArrayList<MasterVO>();
        PreparedStatement pst = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT a.`Plant_Code`, a.`Plant_Name`, IF(a.`Is_Active`='Y','YES','NO') `Is_Active` FROM `t_solar_plant_master` a WHERE a.`Delete_Status`='N' ");
                rs = pst.executeQuery();
                while (rs.next()) {
                    final MasterVO dto = new MasterVO();
                    dto.setPlantCode(rs.getString("Plant_Code"));
                    dto.setPlantname(rs.getString("Plant_Name"));
                    dto.setIsActive(rs.getString("Is_Active"));
                    solarpowerList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException("###Error at AdminDAO[getsolarpwoerList]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return solarpowerList;
    }
    
    public List<MasterVO> gettransmissionList() throws HPSException, HPSSystemException {
        Connection conn = null;
        ResultSet rs = null;
        final List<MasterVO> transmissionList = new ArrayList<MasterVO>();
        PreparedStatement pst = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT a.`Transmission_Code`, a.`Transmission_Name`, IF(a.`Is_Active`='Y','YES','NO') `Is_Active` FROM `t_trasmission_master` a WHERE a.`Delete_Status`='N' ");
                rs = pst.executeQuery();
                while (rs.next()) {
                    final MasterVO dto = new MasterVO();
                    dto.setTransmissionCode(rs.getString("Transmission_Code"));
                    dto.setTransmissionName(rs.getString("Transmission_Name"));
                    dto.setIsActive(rs.getString("Is_Active"));
                    transmissionList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException("###Error at AdminDAO[gettransmissionList]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return transmissionList;
    }
    
    public List<MasterVO> getsubstationList() throws HPSException, HPSSystemException {
        Connection conn = null;
        ResultSet rs = null;
        final List<MasterVO> substationList = new ArrayList<MasterVO>();
        PreparedStatement pst = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT a.`Substation_Code`, a.`Substation_Name`, IF(a.`Is_Active`='Y','YES','NO') `Is_Active` FROM `t_sub_station_master` a WHERE a.`Delete_Status`='N' ");
                rs = pst.executeQuery();
                while (rs.next()) {
                    final MasterVO dto = new MasterVO();
                    dto.setSubstationCode(rs.getString("Substation_Code"));
                    dto.setSubstationName(rs.getString("Substation_Name"));
                    dto.setIsActive(rs.getString("Is_Active"));
                    substationList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException("###Error at AdminDAO[getsubstationList]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return substationList;
    }
    
    public UserDTO getUserDetails(final String uid) throws HPSException, HPSSystemException {
        final UserDTO dto = new UserDTO();
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT a.`User_Id`,a.`Gender`,b.`Role_Id`,e.`Report_Id`,d.`Role_Name`,a.`Name`, a.`Email_Address`,a.`Designation`,a.`Mobile_Number`,a.`Location_Id`, a.`Is_Active`, a.`Created_Date` FROM `t_user_master` a LEFT JOIN `t_user_role_mapping` b ON a.`User_Id` = b.`User_Id` LEFT JOIN `t_role_master` d ON b.`Role_Id` =d.`Role_Id` LEFT JOIN `t_user_report_mapping` e ON a.`User_Id` = e.`User_Id` LEFT JOIN `t_report_master` f ON e.`Report_Id` = f.`Report_Id` WHERE a.User_Id = ? GROUP BY a.User_Id");
                pst.setString(1, uid);
                rs = pst.executeQuery();
                while (rs.next()) {
                    dto.setUserId(uid);
                    dto.setName(rs.getString("Name"));
                    dto.setGender(rs.getString("Gender"));
                    dto.setMobileNumber(rs.getString("Mobile_Number"));
                    dto.setEmailAddress(rs.getString("Email_Address"));
                    dto.setRoleId(rs.getString("Role_Id"));
                    dto.setReportList(rs.getString("Report_Id"));
                    dto.setDesignation(rs.getString("Designation"));
                    dto.setSubStationId(rs.getString("Location_Id"));
                }
            }
        }
        catch (Exception e) {
            throw new HPSException();
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return dto;
    }
    
    public String editUserDtls(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        final ResultSet rs = null;
        String result = "USER_UPDATE_FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            if (conn != null) {
                pst = conn.prepareStatement(" UPDATE `t_user_master` a SET a.`Name` = ?, a.`Gender` = ?,a.`Email_Address`= ?,a.`Mobile_Number` = ?, a.`Designation` = ?,a.`Location_Id` = ?  WHERE a.`User_Id` = ?");
                pst.setString(1, dto.getName());
                pst.setString(2, dto.getGender());
                pst.setString(3, dto.getEmailId());
                pst.setString(4, dto.getMobileNumber());
                pst.setString(5, dto.getDesignation());
                if (dto.getRoleId().equalsIgnoreCase("3")) {
                    pst.setString(6, dto.getSubstationId());
                }
                else {
                    pst.setString(6, null);
                }
                pst.setString(7, dto.getEmailId());
                int count = pst.executeUpdate();
                pst = conn.prepareStatement("DELETE FROM `t_user_role_mapping` WHERE `User_Id` = ?");
                pst.setString(1, dto.getEmailId());
                count = pst.executeUpdate();
                pst = conn.prepareStatement("INSERT INTO `t_user_role_mapping` (`User_Id`, `Role_Id`) VALUES (?, ?)");
                pst.setString(1, dto.getEmailId());
                pst.setString(2, dto.getRoleId());
                count = pst.executeUpdate();
                if (count > 0) {
                    pst = conn.prepareStatement("DELETE FROM `t_user_report_mapping` WHERE `User_Id` = ?");
                    pst.setString(1, dto.getEmailId());
                    count = pst.executeUpdate();
                    if (count >= 0) {
                        for (int i = 0; i < dto.getReportList().length; ++i) {
                            pst = conn.prepareStatement(" INSERT INTO `t_user_report_mapping` (`User_Id`, `Report_Id`) VALUES (?, ?) ");
                            pst.setString(1, dto.getEmailId());
                            pst.setString(2, dto.getReportList()[i]);
                            count = pst.executeUpdate();
                        }
                        result = "USER_UPDATE_SUCCESS";
                        conn.commit();
                    }
                }
            }
        }
        catch (Exception e) {
            conn.rollback();
            result = "USER_UPDATE_FAILURE";
            e.printStackTrace();
            throw new HPSException("### Error at AdminDAO[editUserDtls]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return result;
    }
    
    public String editTariffDtls(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        final ResultSet rs = null;
        String result = "TARIFF_UPDATE_FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
            final java.util.Date date = sdfsource.parse(dto.getTariffSetDate());
            final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
            final String TariffSetDate = sdf.format(date);
            if (conn != null) {
                pst = conn.prepareStatement("UPDATE `t_tariff_master` SET `Plant_Name` =?, `Tariff` =? , `Tariff_Type` = ?, `Tariff_Set_Date` = ? WHERE `Tariff_Code` = ?;");
                pst.setString(1, dto.getPlantname());
                pst.setString(2, dto.getTariff());
                pst.setString(3, dto.getTariffType());
                pst.setString(4, TariffSetDate);
                pst.setString(5, dto.getTariffCode());
                final int count = pst.executeUpdate();
                if (count > 0) {
                    result = "TARIFF_UPDATE_SUCCESS";
                    conn.commit();
                }
            }
        }
        catch (Exception e) {
            conn.rollback();
            result = "TARIFF_UPDATE_FAILURE";
            e.printStackTrace();
            throw new HPSException("### Error at AdminDAO[editTariffDtls]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return result;
    }
    
    public String editWheelingDtls(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        final ResultSet rs = null;
        String result = "WHEELING_UPDATE_FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
            final java.util.Date date = sdfsource.parse(dto.getWheelingSetDate());
            final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
            final String WheelingSetDate = sdf.format(date);
            if (conn != null) {
                pst = conn.prepareStatement(" UPDATE `t_wheeling_master` SET  `Wheeling` = ?, `Wheeling_Set_Date` = ?  WHERE `Wheeling_Code` = ?");
                pst.setString(1, dto.getWheeling());
                pst.setString(2, WheelingSetDate);
                pst.setString(3, dto.getWheelingCode());
                final int count = pst.executeUpdate();
                if (count > 0) {
                    result = "WHEELING_UPDATE_SUCCESS";
                    conn.commit();
                }
            }
        }
        catch (Exception e) {
            conn.rollback();
            result = "WHEELING_UPDATE_FAILURE";
            e.printStackTrace();
            throw new HPSException("### Error at AdminDAO[editWheelingDtls]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return result;
    }
    
    public String editDgPlantDtls(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        final ResultSet rs = null;
        String result = "UPDATE_DG_PLANT_FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
            final java.util.Date date = sdfsource.parse(dto.getOperationDate());
            final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
            final String DgSetDate = sdf.format(date);
            if (conn != null) {
                pst = conn.prepareStatement(" UPDATE `t_dg_set_master` SET `Plant_Name` = ?, `Location` = ?,`Com_Operation_Date` = ?,`Installed_Capacity` = ?  WHERE `Plant_Code` = ? ");
                pst.setString(1, dto.getPlantname());
                pst.setString(2, dto.getPlantlocation());
                pst.setString(3, DgSetDate);
                pst.setString(4, dto.getInstalledcapacity());
                pst.setString(5, dto.getPlantcode());
                final int count = pst.executeUpdate();
                if (count > 0) {
                    result = "UPDATE_DG_PLANT_SUCESS";
                    conn.commit();
                }
            }
        }
        catch (Exception e) {
            conn.rollback();
            result = "UPDATE_DG_PLANT_FAILURE";
            e.printStackTrace();
            throw new HPSException("### Error at AdminDAO[editDgPlantDtls]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return result;
    }
    
    public String editHydropowerPlantDtls(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        final ResultSet rs = null;
        String result = "UPDATE_HYDROPOWER_FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
            final java.util.Date date = sdfsource.parse(dto.getOperationDate());
            final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
            final String HydropowerSetDate = sdf.format(date);
            if (conn != null) {
                pst = conn.prepareStatement(" UPDATE `t_hydro_plant_master` SET `Plant_Name` = ?,  `Location` = ?, `Com_Operation_Date` = ?,  `DPR_Prepared_By` = ?,`DRP_Cost` = ?,`Project_Completion_Cost` = ?, `Installed_Capacity` = ?,  `Design_Energy` = ?, `Units_No` = ?, `Firm_Power` = ?, `Catchment_Area` = ?, `Net_Head` = ?,`Gross_Head` = ?,  `Voltage_Gen` = ?,`Voltage_Trans` = ?, `Switch_Yard` = ?, `Gen_Trans_Capacity` = ?, `No_Ckts` = ?, `No_Bays` = ?, `Switch_Yard_Type` = ?, `Discharge` = ?, `Turbine_Type` = ?,`Loan_Financing` = ?, `Grant_equity` = ?,`Tariff` = ? WHERE `Plant_Code` = ? ");
                pst.setString(1, dto.getPlantname());
                pst.setString(2, dto.getPlantlocation());
                pst.setString(3, HydropowerSetDate);
                pst.setString(4, dto.getDrp());
                pst.setString(5, dto.getPcost());
                pst.setString(6, dto.getComCost());
                pst.setString(7, dto.getInstalledcapacity());
                pst.setString(8, dto.getDesignenegry());
                pst.setString(9, dto.getUnits());
                pst.setString(10, dto.getFirmpower());
                pst.setString(11, dto.getCatchmentarea());
                pst.setString(12, dto.getNethead());
                pst.setString(13, dto.getGrosshead());
                pst.setString(14, dto.getVoltagegen());
                pst.setString(15, dto.getVoltagetrans());
                pst.setString(16, dto.getSwitchyard());
                pst.setString(17, dto.getTrancapacity());
                pst.setString(18, dto.getCkts());
                pst.setString(19, dto.getBays());
                pst.setString(20, dto.getSwitchyardtype());
                pst.setString(21, dto.getDischarge());
                pst.setString(22, dto.getTurbine());
                pst.setString(23, dto.getLoanfinance());
                pst.setString(24, dto.getEquity());
                pst.setString(25, dto.getTariff());
                pst.setString(26, dto.getPlantcode());
                final int count = pst.executeUpdate();
                if (count > 0) {
                    result = "UPDATE_HYDROPOWER_SUCESS";
                    conn.commit();
                }
            }
        }
        catch (Exception e) {
            conn.rollback();
            result = "UPDATE_HYDROPOWER_FAILURE";
            e.printStackTrace();
            throw new HPSException("### Error at AdminDAO[editHydropowerPlantDtls]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return result;
    }
    
    public String editMinihydroPlantDtls(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        final ResultSet rs = null;
        String result = "UPDATE_MINIHYDRO_FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
            final java.util.Date date = sdfsource.parse(dto.getOperationDate());
            final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
            final String minihydropowerSetDate = sdf.format(date);
            if (conn != null) {
                pst = conn.prepareStatement(" UPDATE `t_mini_hydroplant_master` SET `Plant_Name` = ?,  `Location` = ?,  `Com_Operation_Date` = ?, `Installed_Capacity` = ?,  `Design_Energy` = ?,  `Units_No` =?,  `Gross_Head` = ?,  `Voltage_Generation` = ?,  `Voltage_Transmission` = ?,  `Gen_Trans_Capacity` = ?,  `No_Ckts` = ? WHERE `Plant_Code` = ? ");
                pst.setString(1, dto.getPlantname());
                pst.setString(2, dto.getPlantlocation());
                pst.setString(3, minihydropowerSetDate);
                pst.setString(4, dto.getInstalledcapacity());
                pst.setString(5, dto.getDesignenegry());
                pst.setString(6, dto.getUnits());
                pst.setString(7, dto.getGrosshead());
                pst.setString(8, dto.getVoltagegen());
                pst.setString(9, dto.getVoltagetrans());
                pst.setString(10, dto.getTrancapacity());
                pst.setString(11, dto.getCkts());
                pst.setString(12, dto.getPlantcode());
                final int count = pst.executeUpdate();
                if (count > 0) {
                    result = "UPDATE_MINIHYDRO_SUCESS";
                    conn.commit();
                }
            }
        }
        catch (Exception e) {
            conn.rollback();
            result = "UPDATE_MINIHYDRO_FAILURE";
            e.printStackTrace();
            throw new HPSException("### Error at AdminDAO[editMinihydroPlantDtls]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return result;
    }
    
    public String editWindpowerPlantDtls(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        final ResultSet rs = null;
        String result = "UPDATE_WINDPOWER_FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
            final java.util.Date date = sdfsource.parse(dto.getOperationDate());
            final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
            final String windpowerSetDate = sdf.format(date);
            if (conn != null) {
                pst = conn.prepareStatement(" UPDATE `t_wind_plant_master` SET `Plant_Name` = ?,  `Location` = ?, `Com_Operation_Date` = ?,  `Installed_Capacity` = ?,  `Design_Energy` = ? WHERE `Plant_Code` = ?");
                pst.setString(1, dto.getPlantname());
                pst.setString(2, dto.getPlantlocation());
                pst.setString(3, windpowerSetDate);
                pst.setString(4, dto.getInstalledcapacity());
                pst.setString(5, dto.getDesignenegry());
                pst.setString(6, dto.getPlantcode());
                final int count = pst.executeUpdate();
                if (count > 0) {
                    result = "UPDATE_WINDPOWER_SUCCESS";
                    conn.commit();
                }
            }
        }
        catch (Exception e) {
            conn.rollback();
            result = "UPDATE_WINDPOWER_FAILURE";
            e.printStackTrace();
            throw new HPSException("### Error at AdminDAO[editWindpowerPlantDtls]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return result;
    }
    
    public String editSolarpowerPlantDtls(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        final ResultSet rs = null;
        String result = "UPDATE_SOLARPOWER_FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
            final java.util.Date date = sdfsource.parse(dto.getOperationDate());
            final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
            final String solarpowerSetDate = sdf.format(date);
            if (conn != null) {
                pst = conn.prepareStatement(" UPDATE `t_solar_plant_master` SET `Plant_Name` = ?, `Location` = ?, `Com_Operation_Date` = ?, `Installed_Capacity` = ?, `Design_Energy` = ? WHERE `Plant_Code` = ? ");
                pst.setString(1, dto.getPlantname());
                pst.setString(2, dto.getPlantlocation());
                pst.setString(3, solarpowerSetDate);
                pst.setString(4, dto.getInstalledcapacity());
                pst.setString(5, dto.getDesignenegry());
                pst.setString(6, dto.getPlantcode());
                final int count = pst.executeUpdate();
                if (count > 0) {
                    result = "UPDATE_SOLARPOWER_SUCCESS";
                    conn.commit();
                }
            }
        }
        catch (Exception e) {
            conn.rollback();
            result = "UPDATE_SOLARPOWER_FAILURE";
            e.printStackTrace();
            throw new HPSException("### Error at AdminDAO[editSolarpowerPlantDtls]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return result;
    }
    
    public String editTransmissionDtls(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        final ResultSet rs = null;
        String result = "UPDATE_TRANSMISSION_FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            if (conn != null) {
                pst = conn.prepareStatement("UPDATE `t_trasmission_master` SET `Transmission_Name` = ?,`400_kv_dc` = ?,`400_kv_sc` = ?,`220_kv_dc` = ?,`220_kv_sc` = ?,`132_kv_dc` = ?,`132_kv_sc` = ?,`66_kv_dc` = ?,`66_kv_sc` = ?,`66_kv_qc` = ?,`UG` = ?,`Type_of_Conductor` = ?,`Remarks` = ?,WHERE `Transmission_Code` = ?");
                pst.setString(1, dto.getPlantname());
                pst.setString(2, dto.getPlantlocation());
                pst.setString(3, dto.getDrp());
                pst.setString(4, dto.getPcost());
                pst.setString(5, dto.getInstalledcapacity());
                pst.setString(6, dto.getDesignenegry());
                pst.setString(7, dto.getUnits());
                pst.setString(8, dto.getFirmpower());
                pst.setString(9, dto.getGrosshead());
                pst.setString(10, dto.getVoltagegen());
                pst.setString(11, dto.getVoltagetrans());
                pst.setString(12, dto.getTurbine());
                pst.setString(13, dto.getSwitchyard());
                pst.setString(14, dto.getTransmissionCode());
                final int count = pst.executeUpdate();
                if (count > 0) {
                    result = "UPDATE_TRANSMISSION_SUCCESS";
                    conn.commit();
                }
            }
        }
        catch (Exception e) {
            conn.rollback();
            result = "UPDATE_TRANSMISSION_FAILURE";
            e.printStackTrace();
            throw new HPSException("### Error at AdminDAO[editTransmissionDtls]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return result;
    }
    
    public String editSubStationDtls(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        final ResultSet rs = null;
        String result = "UPDATE_SUB_STATION_FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
            final java.util.Date date = sdfsource.parse(dto.getOperationDate());
            final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
            final String subStationSetDate = sdf.format(date);
            if (conn != null) {
                pst = conn.prepareStatement(" UPDATE `t_sub_station_master` SET `Substation_Name` = ?, `Location` = ?, `Com_Operation_Date` = ?,`Capacity` = ?,`Area` = ? WHERE `Substation_Code` = ? ");
                pst.setString(1, dto.getPlantname());
                pst.setString(2, dto.getPlantlocation());
                pst.setString(3, subStationSetDate);
                pst.setString(4, dto.getInstalledcapacity());
                pst.setString(5, dto.getDesignenegry());
                pst.setString(6, dto.getSubStationCode());
                final int count = pst.executeUpdate();
                if (count > 0) {
                    result = "UPDATE_SUB_STATION_SUCESS";
                    conn.commit();
                }
            }
        }
        catch (Exception e) {
            conn.rollback();
            result = "UPDATE_SUB_STATION_FAILURE";
            e.printStackTrace();
            throw new HPSException("### Error at AdminDAO[editTransmissionDtls]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return result;
    }
    
    public String userManagement(final String uid, final String identifier) throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        final ResultSet rs = null;
        String result = "FAILURE";
        String query = null;
        try {
            if (identifier.equalsIgnoreCase("DELETE_USER")) {
                query = "UPDATE t_user_master a SET a.`Logical_Delete` = ? WHERE a.`User_Id` = ?";
            }
            else if (identifier.equalsIgnoreCase("DEACTIVATE_USER")) {
                query = "UPDATE t_user_master a SET a.`Is_Active` = ? WHERE a.`User_Id` = ?";
            }
            else if (identifier.equalsIgnoreCase("ACTIVATE_USER")) {
                query = "UPDATE t_user_master a SET a.`Is_Active` = ? WHERE a.`User_Id` = ?";
            }
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            if (conn != null) {
                pst = conn.prepareStatement(query);
                if (identifier.equalsIgnoreCase("DELETE_USER")) {
                    pst.setString(1, "Y");
                    pst.setString(2, uid);
                }
                else if (identifier.equalsIgnoreCase("DEACTIVATE_USER")) {
                    pst.setString(1, "N");
                    pst.setString(2, uid);
                }
                else if (identifier.equalsIgnoreCase("ACTIVATE_USER")) {
                    pst.setString(1, "Y");
                    pst.setString(2, uid);
                }
                final int count = pst.executeUpdate();
                if (count > 0) {
                    result = "SUCCESS";
                    conn.commit();
                }
            }
        }
        catch (Exception e) {
            conn.rollback();
            result = "FAILURE";
            throw new HPSException("###Error at AdminDAO[userManagement]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return result;
    }
    
    public MasterVO getfeedbackdetails(final String id) throws HPSException, HPSSystemException {
        final MasterVO dto = new MasterVO();
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        try {
            conn = ConnectionManager.getConnection();
            pst = conn.prepareStatement("SELECT a.`Name`,a.`Address`,a.`Email_Id`,a.`FeedBack` FROM `t_feedback_tbl`a  WHERE `FeedBack_Id` = ?");
            pst.setString(1, id);
            rs = pst.executeQuery();
            while (rs.next()) {
                dto.setName(rs.getString("Name"));
                dto.setAddress(rs.getString("Address"));
                dto.setEmailId(rs.getString("Email_Id"));
                dto.setFeedback(rs.getString("FeedBack"));
            }
        }
        catch (Exception e) {
            throw new HPSException();
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return dto;
    }
    
    public ApplicationDataVO getErrorDetails(final ApplicationDataVO appVO) throws HPSException, HPSSystemException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        try {
            conn = ConnectionManager.getConnection();
            pst = conn.prepareStatement("SELECT Error_Details FROM t_error_details WHERE Error_Code=?");
            pst.setString(1, appVO.getErrorCode());
            rs = pst.executeQuery();
            if (rs != null && rs.first()) {
                appVO.setErrorDetails(rs.getString("Error_Details"));
            }
        }
        catch (Exception e) {
            throw new HPSException("### Error at AdminDAO[getErrorDetails]: exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return appVO;
    }
    
    public String addMenu(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        int menuId = 0;
        int parentMenuSecId = 0;
        int childMenuId = 0;
        String result = "FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            if (conn != null) {
                pst = conn.prepareStatement("SELECT a.`Menu_Id` FROM `t_menu_master` a ORDER  BY a.`Menu_Id` DESC LIMIT  1");
                rs = pst.executeQuery();
                rs.first();
                menuId = rs.getInt("Menu_Id");
                if (++menuId != 0) {
                    pst = conn.prepareStatement("INSERT INTO t_menu_content (`Menu_Id`,`Content`,`Display_Status`,`Created_Date`) VALUES (?,?,?,?)");
                    pst.setInt(1, menuId);
                    pst.setString(2, dto.getContent());
                    pst.setString(3, "Y");
                    pst.setDate(4, AdminDAO.date);
                    pst.executeUpdate();
                    if (dto.getMenuType().equalsIgnoreCase("parent")) {
                        pst = conn.prepareStatement("SELECT a.`Parent_Menu_Sequence` FROM `t_menu_master` a WHERE a.`Menu_Cat_Type` = 'P' ORDER  BY a.`Parent_Menu_Sequence` DESC LIMIT  1");
                        rs = pst.executeQuery();
                        rs.first();
                        parentMenuSecId = rs.getInt("Parent_Menu_Sequence");
                        ++parentMenuSecId;
                        pst = conn.prepareStatement("INSERT INTO `t_menu_master`(`Menu_Id`,`Menu_Cat_Type`,`Parent_Menu_Id`,`Menu_Name`,`Parent_Menu_Sequence`,Menu_Sequence_No,`Menu_Type`,`Is_Active`) VALUES (?,?,?,?,?,?,?,?);");
                        pst.setInt(1, menuId);
                        pst.setString(2, "P");
                        pst.setInt(3, menuId);
                        pst.setString(4, dto.getTitle());
                        pst.setInt(5, parentMenuSecId);
                        pst.setString(6, HPSConstants.STRING_NULL);
                        pst.setString(7, "P");
                        pst.setString(8, "Y");
                        pst.executeUpdate();
                    }
                    else {
                        pst = conn.prepareStatement("SELECT a.`Menu_Sequence_No` FROM `t_menu_master` a WHERE a.`Menu_Type`= 'S' AND a.`Parent_Menu_Id` = ? ORDER  BY a.`Menu_Sequence_No` DESC LIMIT  1");
                        pst.setString(1, dto.getParentMenuId());
                        rs = pst.executeQuery();
                        rs.first();
                        if (!rs.next()) {
                            childMenuId = 0;
                        }
                        else {
                            childMenuId = rs.getInt("Menu_Sequence_No");
                        }
                        ++childMenuId;
                        pst = conn.prepareStatement("INSERT INTO `t_menu_master`(`Menu_Id`,`Menu_Cat_Type`,`Parent_Menu_Id`,`Menu_Name`,`Parent_Menu_Sequence`,Menu_Sequence_No,`Menu_Type`,`Is_Active`) VALUES (?,?,?,?,?,?,?,?);");
                        pst.setInt(1, menuId);
                        pst.setString(2, "P");
                        pst.setString(3, dto.getParentMenuId());
                        pst.setString(4, dto.getTitle());
                        pst.setString(5, HPSConstants.STRING_NULL);
                        pst.setInt(6, childMenuId);
                        pst.setString(7, "S");
                        pst.setString(8, "Y");
                        pst.executeUpdate();
                    }
                    result = "SUCCESS";
                }
            }
        }
        catch (Exception e) {
            conn.rollback();
            result = "FAILURE";
            throw new HPSException("###Error at AdminDAO[addMenu]: exception:: " + e);
        }
        finally {
            conn.setAutoCommit(true);
            ConnectionManager.close(conn, (ResultSet)null, pst);
        }
        conn.setAutoCommit(true);
        ConnectionManager.close(conn, (ResultSet)null, pst);
        return result;
    }
    
    public String addtariff(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException, ParseException {
        Connection conn = null;
        PreparedStatement pst = null;
        String query = null;
        String result = "FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
            final java.util.Date date = sdfsource.parse(dto.getTariffSetDate());
            final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
            final String TariffSetDate = sdf.format(date);
            query = " INSERT INTO `t_tariff_master`(`Plant_Name`,`Tariff`, `Tariff_Type`, `Tariff_Set_Date`,`Is_Active`)VALUES (?,?,?,?,?) ";
            pst = conn.prepareStatement(query);
            pst.setString(1, dto.getPlantname());
            pst.setString(2, dto.getTariff());
            pst.setString(3, dto.getTariffType());
            pst.setString(4, TariffSetDate);
            pst.setString(5, "Y");
            pst.executeUpdate();
            conn.commit();
            result = "Success";
        }
        catch (SQLException e) {
            conn.rollback();
            result = "FAILURE";
            throw new HPSException("###Error at AdminDAO[addTariff]: exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, (ResultSet)null, pst);
        }
        ConnectionManager.close(conn, (ResultSet)null, pst);
        return result;
    }
    
    public String addwheeling(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException, ParseException {
        Connection conn = null;
        PreparedStatement pst = null;
        String query = null;
        String result = "FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
            final java.util.Date date = sdfsource.parse(dto.getWheelingSetDate());
            final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
            final String WheelingSetDate = sdf.format(date);
            query = " INSERT INTO `t_wheeling_master` (`Wheeling`,`Wheeling_Set_Date`,`Is_Active`)VALUES (?,?,?) ";
            pst = conn.prepareStatement(query);
            pst.setString(1, dto.getWheeling());
            pst.setString(2, WheelingSetDate);
            pst.setString(3, "Y");
            pst.executeUpdate();
            conn.commit();
            result = "Success";
        }
        catch (SQLException e) {
            conn.rollback();
            result = "FAILURE";
            throw new HPSException("###Error at AdminDAO[addWheeling]: exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, (ResultSet)null, pst);
        }
        ConnectionManager.close(conn, (ResultSet)null, pst);
        return result;
    }
    
    public String adddg(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException, ParseException {
        Connection conn = null;
        PreparedStatement pst = null;
        String query = null;
        String result = "FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
            final java.util.Date date = sdfsource.parse(dto.getOperationDate());
            final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
            final String DgSetDate = sdf.format(date);
            query = " INSERT INTO `t_dg_set_master` (`Plant_Name`,`Location`,`Installed_Capacity`,`Com_Operation_Date`,`Is_Active`)VALUES (?,?,?,?,?) ";
            pst = conn.prepareStatement(query);
            pst.setString(1, dto.getPlantname());
            pst.setString(2, dto.getPlantlocation());
            pst.setString(3, dto.getInstalledcapacity());
            pst.setString(4, DgSetDate);
            pst.setString(5, "Y");
            pst.executeUpdate();
            conn.commit();
            result = "Success";
        }
        catch (SQLException e) {
            conn.rollback();
            result = "FAILURE";
            throw new HPSException("###Error at AdminDAO[adddg]: exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, (ResultSet)null, pst);
        }
        ConnectionManager.close(conn, (ResultSet)null, pst);
        return result;
    }
    
    public String addhydropower(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException, ParseException {
        Connection conn = null;
        PreparedStatement pst = null;
        String query = null;
        String result = "FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
            final java.util.Date date = sdfsource.parse(dto.getOperationDate());
            final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
            final String HydropowerSetDate = sdf.format(date);
            query = " INSERT INTO `t_hydro_plant_master`(`Plant_Name`,`Location`,`Com_Operation_Date`,`DPR_Prepared_By`,`DRP_Cost`,`Project_Completion_Cost`,`Installed_Capacity`,`Design_Energy`,`Units_No`,`Firm_Power`,`Catchment_Area`,`Net_Head`,`Gross_Head`,`Voltage_Gen`,`Voltage_Trans`,`Switch_Yard`,`Gen_Trans_Capacity`,`No_Ckts`,`No_Bays`,`Switch_Yard_Type`,`Discharge`,`Turbine_Type`,`Loan_Financing`,`Grant_equity`,`Tariff`,`Is_Active`) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ";
            pst = conn.prepareStatement(query);
            pst.setString(1, dto.getPlantname());
            pst.setString(2, dto.getPlantlocation());
            pst.setString(3, HydropowerSetDate);
            pst.setString(4, dto.getDrp());
            pst.setString(5, dto.getPcost());
            pst.setString(6, dto.getComCost());
            pst.setString(7, dto.getInstalledcapacity());
            pst.setString(8, dto.getDesignenegry());
            pst.setString(9, dto.getUnits());
            pst.setString(10, dto.getFirmpower());
            pst.setString(11, dto.getCatchmentarea());
            pst.setString(12, dto.getNethead());
            pst.setString(13, dto.getGrosshead());
            pst.setString(14, dto.getVoltagegen());
            pst.setString(15, dto.getVoltagetrans());
            pst.setString(16, dto.getSwitchyard());
            pst.setString(17, dto.getTrancapacity());
            pst.setString(18, dto.getCkts());
            pst.setString(19, dto.getBays());
            pst.setString(20, dto.getSwitchyardtype());
            pst.setString(21, dto.getDischarge());
            pst.setString(22, dto.getTurbine());
            pst.setString(23, dto.getLoanfinance());
            pst.setString(24, dto.getEquity());
            pst.setString(25, dto.getTariff());
            pst.setString(26, "Y");
            pst.executeUpdate();
            conn.commit();
            result = "Success";
        }
        catch (SQLException e) {
            conn.rollback();
            result = "FAILURE";
            throw new HPSException("###Error at AdminDAO[addhydropower]: exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, (ResultSet)null, pst);
        }
        ConnectionManager.close(conn, (ResultSet)null, pst);
        return result;
    }
    
    public String addminihydropower(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException, ParseException {
        Connection conn = null;
        PreparedStatement pst = null;
        String query = null;
        String result = "FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
            final java.util.Date date = sdfsource.parse(dto.getOperationDate());
            final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
            final String minihydropowerSetDate = sdf.format(date);
            query = " INSERT INTO `t_mini_hydroplant_master`(`Plant_Name`,`Location`,`Com_Operation_Date`,`Installed_Capacity`,`Design_Energy`,`Units_No`,`Gross_Head`,`Voltage_Generation`,`Voltage_Transmission`,`Gen_Trans_Capacity`,`No_Ckts`,`Is_Active`)VALUES (?,?,?,?,?,?,?,?,?,?,?,?); ";
            pst = conn.prepareStatement(query);
            pst.setString(1, dto.getPlantname());
            pst.setString(2, dto.getPlantlocation());
            pst.setString(3, minihydropowerSetDate);
            pst.setString(4, dto.getInstalledcapacity());
            pst.setString(5, dto.getDesignenegry());
            pst.setString(6, dto.getUnits());
            pst.setString(7, dto.getGrosshead());
            pst.setString(8, dto.getVoltagegen());
            pst.setString(9, dto.getVoltagetrans());
            pst.setString(10, dto.getTrancapacity());
            pst.setString(11, dto.getCkts());
            pst.setString(12, "Y");
            pst.executeUpdate();
            conn.commit();
            result = "Success";
        }
        catch (SQLException e) {
            conn.rollback();
            result = "FAILURE";
            throw new HPSException("###Error at AdminDAO[addminihydropower]: exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, (ResultSet)null, pst);
        }
        ConnectionManager.close(conn, (ResultSet)null, pst);
        return result;
    }
    
    public String addwindpower(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException, ParseException {
        Connection conn = null;
        PreparedStatement pst = null;
        String query = null;
        String result = "FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
            final java.util.Date date = sdfsource.parse(dto.getOperationDate());
            final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
            final String windpowerSetDate = sdf.format(date);
            query = " INSERT INTO `t_wind_plant_master`(`Plant_Name`,`Location`,`Com_Operation_Date`,`Installed_Capacity`,`Design_Energy`,`Is_Active`)VALUES (?,?,?,?,?,?) ";
            pst = conn.prepareStatement(query);
            pst.setString(1, dto.getPlantname());
            pst.setString(2, dto.getPlantlocation());
            pst.setString(3, windpowerSetDate);
            pst.setString(4, dto.getInstalledcapacity());
            pst.setString(5, dto.getDesignenegry());
            pst.setString(6, "Y");
            pst.executeUpdate();
            conn.commit();
            result = "Success";
        }
        catch (SQLException e) {
            conn.rollback();
            result = "FAILURE";
            throw new HPSException("###Error at AdminDAO[addwindpower]: exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, (ResultSet)null, pst);
        }
        ConnectionManager.close(conn, (ResultSet)null, pst);
        return result;
    }
    
    public String addsolarpower(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException, ParseException {
        Connection conn = null;
        PreparedStatement pst = null;
        String query = null;
        String result = "FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
            final java.util.Date date = sdfsource.parse(dto.getOperationDate());
            final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
            final String solarpowerSetDate = sdf.format(date);
            query = " INSERT INTO `t_solar_plant_master`(`Plant_Name`,`Location`,`Com_Operation_Date`,`Installed_Capacity`,`Design_Energy`,`Is_Active`)VALUES (?,?,?,?,?,?) ";
            pst = conn.prepareStatement(query);
            pst.setString(1, dto.getPlantname());
            pst.setString(2, dto.getPlantlocation());
            pst.setString(3, solarpowerSetDate);
            pst.setString(4, dto.getInstalledcapacity());
            pst.setString(5, dto.getDesignenegry());
            pst.setString(6, "Y");
            pst.executeUpdate();
            conn.commit();
            result = "Success";
        }
        catch (SQLException e) {
            conn.rollback();
            result = "FAILURE";
            throw new HPSException("###Error at AdminDAO[addwindpower]: exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, (ResultSet)null, pst);
        }
        ConnectionManager.close(conn, (ResultSet)null, pst);
        return result;
    }
    
    public String addtransmission(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException, ParseException {
        Connection conn = null;
        PreparedStatement pst = null;
        String query = null;
        String result = "FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            query = " INSERT INTO `t_trasmission_master`(`Transmission_Name`,`400_kv_dc`,`400_kv_sc`,`220_kv_dc`,`220_kv_sc`,`132_kv_dc`,`132_kv_sc`,`66_kv_dc`,`66_kv_sc`,`66_kv_qc`,`UG`,`Type_of_Conductor`,`Remarks`,`Is_Active`)VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?) ";
            pst = conn.prepareStatement(query);
            pst.setString(1, dto.getPlantname());
            pst.setString(2, dto.getPlantlocation());
            pst.setString(3, dto.getDrp());
            pst.setString(4, dto.getPcost());
            pst.setString(5, dto.getInstalledcapacity());
            pst.setString(6, dto.getDesignenegry());
            pst.setString(7, dto.getUnits());
            pst.setString(8, dto.getFirmpower());
            pst.setString(9, dto.getGrosshead());
            pst.setString(10, dto.getVoltagegen());
            pst.setString(11, dto.getVoltagetrans());
            pst.setString(12, dto.getTurbine());
            pst.setString(13, dto.getSwitchyard());
            pst.setString(14, "Y");
            final DecimalFormat dto2 = new DecimalFormat("0.00");
            dto2.setMaximumFractionDigits(2);
            pst.executeUpdate();
            conn.commit();
            result = "Success";
        }
        catch (SQLException e) {
            conn.rollback();
            result = "FAILURE";
            throw new HPSException("###Error at AdminDAO[addtransmission]: exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, (ResultSet)null, pst);
        }
        ConnectionManager.close(conn, (ResultSet)null, pst);
        return result;
    }
    
    public String addsubstation(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException, ParseException {
        Connection conn = null;
        PreparedStatement pst = null;
        String query = null;
        String result = "FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
            final java.util.Date date = sdfsource.parse(dto.getOperationDate());
            final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
            final String subStationSetDate = sdf.format(date);
            query = " INSERT INTO `t_sub_station_master`(`Substation_Name`,`Location`,`Com_Operation_Date`,`Capacity`,`Transformer`,`Voltage_Ratio`,`Area`,`Is_Active`)VALUES (?,?,?,?,?,?,?,?) ";
            pst = conn.prepareStatement(query);
            pst.setString(1, dto.getPlantname());
            pst.setString(2, dto.getPlantlocation());
            pst.setString(3, subStationSetDate);
            pst.setString(4, dto.getInstalledcapacity());
            pst.setString(5, dto.getVoltagegen());
            pst.setString(6, dto.getTrancapacity());
            pst.setString(7, dto.getDesignenegry());
            pst.setString(8, "Y");
            pst.executeUpdate();
            conn.commit();
            result = "Success";
        }
        catch (SQLException e) {
            conn.rollback();
            result = "FAILURE";
            throw new HPSException("###Error at AdminDAO[addsub_station]: exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, (ResultSet)null, pst);
        }
        ConnectionManager.close(conn, (ResultSet)null, pst);
        return result;
    }
    
    public List<MenuVO> getChildMenuList(final String Id) throws HPSException, HPSSystemException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        final List<MenuVO> menuList = new ArrayList<MenuVO>();
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement("SELECT a.`Menu_Id`,a.`Menu_Name`,IF(a.`Is_Active`='Y','YES','NO') Is_Active,a.`Parent_Menu_Id` FROM `t_menu_master` a WHERE a.`Parent_Menu_Id` =? AND a.`Menu_Type` ='S' AND a.`Is_Deleted` = 'N' ORDER BY a.`Menu_Sequence_No` ASC");
                pst.setString(1, Id);
                rs = pst.executeQuery();
                while (rs.next()) {
                    final MenuVO dto = new MenuVO();
                    dto.setMenuId(rs.getString("Menu_Id"));
                    dto.setParentMenuId(rs.getString("Parent_Menu_Id"));
                    dto.setMenuName(rs.getString("Menu_Name"));
                    dto.setIsActive(rs.getString("Is_Active"));
                    menuList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException("###Error at AdminDAO[getPublicMenuList]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return menuList;
    }
    
    public String portalManagement(final String id, final String identifier, final String type) throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        final ResultSet rs = null;
        String result = "FAILURE";
        String query = null;
        try {
            if (identifier.equalsIgnoreCase("MENU") && type.equalsIgnoreCase("DEACTIVATE")) {
                query = "UPDATE `t_menu_master` a SET a.`Is_Active` = ? WHERE a.`Menu_Id` = ?";
            }
            if (identifier.equalsIgnoreCase("MENU") && type.equalsIgnoreCase("ACTIVATE")) {
                query = "UPDATE `t_menu_master` a SET a.`Is_Active` = ? WHERE a.`Menu_Id` = ?";
            }
            if (type.equalsIgnoreCase("DELETE") && identifier.equalsIgnoreCase("MENU")) {
                query = "UPDATE `t_menu_master` a SET a.`Is_Active` = ? ,a.`Is_Deleted` = ? WHERE a.`Menu_Id` = ?";
            }
            if (identifier.equalsIgnoreCase("TARIFF") && type.equalsIgnoreCase("DEACTIVATE")) {
                query = " UPDATE `t_tariff_master` a SET a.`Is_Active` = ? WHERE a.`Tariff_Code` = ? ";
            }
            if (identifier.equalsIgnoreCase("TARIFF") && type.equalsIgnoreCase("ACTIVATE")) {
                query = " UPDATE `t_tariff_master` a SET a.`Is_Active` = ? WHERE a.`Tariff_Code` = ? ";
            }
            if (type.equalsIgnoreCase("DELETE") && identifier.equalsIgnoreCase("TARIFF")) {
                query = " UPDATE `t_tariff_master` a SET a.`Is_Active` = ? ,a.`Delete_Status` = ? WHERE a.`Tariff_Code` = ? ";
            }
            if (identifier.equalsIgnoreCase("WHEELING") && type.equalsIgnoreCase("DEACTIVATE")) {
                query = " UPDATE `t_wheeling_master` a SET a.`Is_Active` = ? WHERE a.`Wheeling_Code` = ? ";
            }
            if (identifier.equalsIgnoreCase("WHEELING") && type.equalsIgnoreCase("ACTIVATE")) {
                query = " UPDATE `t_wheeling_master` a SET a.`Is_Active` = ? WHERE a.`Wheeling_Code` = ? ";
            }
            if (type.equalsIgnoreCase("DELETE") && identifier.equalsIgnoreCase("WHEELING")) {
                query = " UPDATE `t_wheeling_master` a SET a.`Is_Active` = ? ,a.`Delete_Status` = ? WHERE a.`Wheeling_Code` = ? ";
            }
            if (identifier.equalsIgnoreCase("DG") && type.equalsIgnoreCase("DEACTIVATE")) {
                query = " UPDATE `t_dg_set_master` a SET a.`Is_Active` = ? WHERE a.`Plant_Code` = ? ";
            }
            if (identifier.equalsIgnoreCase("DG") && type.equalsIgnoreCase("ACTIVATE")) {
                query = " UPDATE `t_dg_set_master` a SET a.`Is_Active` = ? WHERE a.`Plant_Code` = ? ";
            }
            if (type.equalsIgnoreCase("DELETE") && identifier.equalsIgnoreCase("DG")) {
                query = " UPDATE `t_dg_set_master` a SET a.`Is_Active` = ? ,a.`Delete_Status` = ? WHERE a.`Plant_Code` = ?";
            }
            if (identifier.equalsIgnoreCase("HYDROPOWER") && type.equalsIgnoreCase("DEACTIVATE")) {
                query = " UPDATE `t_hydro_plant_master` a SET a.`Is_Active` = ? WHERE a.`Plant_Code` = ? ";
            }
            if (identifier.equalsIgnoreCase("HYDROPOWER") && type.equalsIgnoreCase("ACTIVATE")) {
                query = " UPDATE `t_hydro_plant_master` a SET a.`Is_Active` = ? WHERE a.`Plant_Code` = ? ";
            }
            if (type.equalsIgnoreCase("DELETE") && identifier.equalsIgnoreCase("HYDROPOWER")) {
                query = " UPDATE `t_hydro_plant_master` a SET a.`Is_Active` = ? ,a.`Delete_Status` = ? WHERE a.`Plant_Code` = ? ";
            }
            if (identifier.equalsIgnoreCase("MINIHYDROPOWER") && type.equalsIgnoreCase("DEACTIVATE")) {
                query = " UPDATE `t_mini_hydroplant_master` a SET a.`Is_Active` = ? WHERE a.`Plant_Code` = ? ";
            }
            if (identifier.equalsIgnoreCase("MINIHYDROPOWER") && type.equalsIgnoreCase("ACTIVATE")) {
                query = " UPDATE `t_mini_hydroplant_master` a SET a.`Is_Active` = ? WHERE a.`Plant_Code` = ? ";
            }
            if (type.equalsIgnoreCase("DELETE") && identifier.equalsIgnoreCase("MINIHYDROPOWER")) {
                query = " UPDATE `t_mini_hydroplant_master` a SET a.`Is_Active` = ? ,a.`Delete_Status` = ? WHERE a.`Plant_Code` = ? ";
            }
            if (identifier.equalsIgnoreCase("WINDPOWER") && type.equalsIgnoreCase("DEACTIVATE")) {
                query = " UPDATE `t_wind_plant_master` a SET a.`Is_Active` = ? WHERE a.`Plant_Code` = ? ";
            }
            if (identifier.equalsIgnoreCase("WINDPOWER") && type.equalsIgnoreCase("ACTIVATE")) {
                query = " UPDATE `t_wind_plant_master` a SET a.`Is_Active` = ? WHERE a.`Plant_Code` = ? ";
            }
            if (type.equalsIgnoreCase("DELETE") && identifier.equalsIgnoreCase("WINDPOWER")) {
                query = " UPDATE `t_wind_plant_master` a SET a.`Is_Active` = ? ,a.`Delete_Status` = ? WHERE a.`Plant_Code` = ? ";
            }
            if (identifier.equalsIgnoreCase("SOLARPOWER") && type.equalsIgnoreCase("DEACTIVATE")) {
                query = " UPDATE `t_solar_plant_master` a SET a.`Is_Active` = ? WHERE a.`Plant_Code` = ? ";
            }
            if (identifier.equalsIgnoreCase("SOLARPOWER") && type.equalsIgnoreCase("ACTIVATE")) {
                query = " UPDATE `t_solar_plant_master` a SET a.`Is_Active` = ? WHERE a.`Plant_Code` = ? ";
            }
            if (type.equalsIgnoreCase("DELETE") && identifier.equalsIgnoreCase("SOLARPOWER")) {
                query = " UPDATE `t_solar_plant_master` a SET a.`Is_Active` = ? ,a.`Delete_Status` = ? WHERE a.`Plant_Code` = ? ";
            }
            if (identifier.equalsIgnoreCase("TRANSMISSION") && type.equalsIgnoreCase("DEACTIVATE")) {
                query = " UPDATE `t_trasmission_master` a SET a.`Is_Active` = ? WHERE a.`Transmission_Code` = ? ";
            }
            if (identifier.equalsIgnoreCase("TRANSMISSION") && type.equalsIgnoreCase("ACTIVATE")) {
                query = " UPDATE `t_trasmission_master` a SET a.`Is_Active` = ? WHERE a.`Transmission_Code` = ? ";
            }
            if (type.equalsIgnoreCase("DELETE") && identifier.equalsIgnoreCase("TRANSMISSION")) {
                query = " UPDATE `t_trasmission_master` a SET a.`Is_Active` = ? ,a.`Delete_Status` = ? WHERE a.`Transmission_Code` = ? ";
            }
            if (identifier.equalsIgnoreCase("SUB_STATION") && type.equalsIgnoreCase("DEACTIVATE")) {
                query = " UPDATE `t_sub_station_master` a SET a.`Is_Active` = ? WHERE a.`Substation_Code` = ? ";
            }
            if (identifier.equalsIgnoreCase("SUB_STATION") && type.equalsIgnoreCase("ACTIVATE")) {
                query = " UPDATE `t_sub_station_master` a SET a.`Is_Active` = ? WHERE a.`Substation_Code` = ? ";
            }
            if (type.equalsIgnoreCase("DELETE") && identifier.equalsIgnoreCase("SUB_STATION")) {
                query = " UPDATE `t_sub_station_master` a SET a.`Is_Active` = ? ,a.`Delete_Status` = ? WHERE a.`Substation_Code` = ? ";
            }
            if (type.equalsIgnoreCase("DELETE") && identifier.equalsIgnoreCase("FEEDBACK")) {
                query = "UPDATE `t_feedback_tbl` a SET a.`Is_Active` = ?, a.`Delete_Status` = ? WHERE a.`FeedBack_Id`= ?";
            }
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            if (conn != null) {
                pst = conn.prepareStatement(query);
                if (type.equalsIgnoreCase("DEACTIVATE")) {
                    pst.setString(1, "N");
                    pst.setString(2, id);
                }
                if (type.equalsIgnoreCase("ACTIVATE")) {
                    pst.setString(1, "Y");
                    pst.setString(2, id);
                }
                if (type.equalsIgnoreCase("DELETE")) {
                    pst.setString(1, "N");
                    pst.setString(2, "Y");
                    pst.setString(3, id);
                }
                final int count = pst.executeUpdate();
                if (count > 0) {
                    result = "SUCCESS";
                    conn.commit();
                }
            }
        }
        catch (Exception e) {
            conn.rollback();
            result = "FAILURE";
            throw new HPSException("###Error at AdminDAO[portalManagement]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return result;
    }
    
    public static String editContent(final AdminDTO dto) throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        final ResultSet rs = null;
        String result = "FAILURE";
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            if (conn != null) {
                if (dto.getType().equalsIgnoreCase("MENU")) {
                    pst = conn.prepareStatement("UPDATE t_menu_master a LEFT JOIN t_menu_content b ON a.menu_id=b.menu_id SET a.menu_name=?,b.content=? WHERE a.menu_id=?");
                    pst.setString(1, dto.getEditedTitle());
                    pst.setString(2, dto.getEditedContent());
                    pst.setString(3, dto.getId());
                }
                else if (dto.getType().equalsIgnoreCase("ANNOUNCEMENT")) {
                    pst = conn.prepareStatement("UPDATE t_announcement_dtls SET announcement_title=?,announcement_content=? WHERE announcement_id=?");
                    pst.setString(1, dto.getEditedTitle());
                    pst.setString(2, dto.getEditedContent());
                    pst.setString(3, dto.getId());
                }
                pst.executeUpdate();
            }
        }
        catch (Exception e) {
            conn.rollback();
            result = "FAILURE";
            throw new HPSException("###Error at AdminDAO[addMenu]: exception:: " + e);
        }
        finally {
            result = "SUCCESS";
            conn.setAutoCommit(true);
            ConnectionManager.close(conn, rs, pst);
        }
        result = "SUCCESS";
        conn.setAutoCommit(true);
        ConnectionManager.close(conn, rs, pst);
        return result;
    }
    
    public static AdminDTO getContent(final String id, final String type) throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        final AdminDTO dto = new AdminDTO();
        try {
            conn = ConnectionManager.getConnection();
            pst = conn.prepareStatement("SELECT a.`Menu_Name` title,b.`Content` FROM `t_menu_master` a LEFT JOIN `t_menu_content` b ON a.`Menu_Id`=b.`Menu_Id` WHERE a.Menu_Id=? AND a.`Menu_Cat_Type`=?");
            pst.setString(1, id);
            pst.setString(2, "P");
            rs = pst.executeQuery();
            rs.first();
            dto.setEditedTitle(rs.getString("title"));
            dto.setEditedContent(rs.getString("content"));
            dto.setId(id);
            dto.setType(type);
            dto.setGlobalTitle("News");
        }
        catch (Exception e) {
            System.out.println("####### Error in AddContentDAO[getContent]: " + e);
            return dto;
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return dto;
    }
    
    public List<MasterVO> getFeedbacklist() throws HPSException, HPSSystemException {
        Connection conn = null;
        ResultSet rs = null;
        final List<MasterVO> feedbackList = new ArrayList<MasterVO>();
        PreparedStatement pst = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement("SELECT a.FeedBack_Id,a.`Name`,a.`Address`,a.`Email_Id`,a.`FeedBack`,IF(a.`Is_Active`='Y','YES','NO') `Is_Active`  FROM `t_feedback_tbl`a WHERE a.`Delete_Status` ='N'");
                rs = pst.executeQuery();
                while (rs.next()) {
                    final MasterVO dto = new MasterVO();
                    dto.setFeedbackId(rs.getString("FeedBack_Id"));
                    dto.setName(rs.getString("Name"));
                    dto.setAddress(rs.getString("Address"));
                    dto.setEmailId(rs.getString("Email_Id"));
                    dto.setFeedback(rs.getString("FeedBack"));
                    feedbackList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException("###Error at AdminDAO[gettariffList]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return feedbackList;
    }
    
    public List<ReportDTO> gettransimissionlist() throws HPSException, HPSSystemException {
        Connection conn = null;
        ResultSet rs = null;
        final List<ReportDTO> reportList = new ArrayList<ReportDTO>();
        PreparedStatement pst = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement("SELECT a.`Transmission_Name`, a.`400_kv_dc`,a.`400_kv_sc`,a.`220_kv_dc`,a.`220_kv_sc`,a.`132_kv_dc`,a.`132_kv_sc`,a.`66_kv_dc`,a.`66_kv_sc`,a.`66_kv_qc`,a.`UG`,a.`Remarks` FROM `t_trasmission_master`a ");
                rs = pst.executeQuery();
                while (rs.next()) {
                    final ReportDTO dto = new ReportDTO();
                    dto.setPlantname(rs.getString("Transmission_Name"));
                    dto.setPlantlocation(rs.getString("400_kv_dc"));
                    dto.setDrp(rs.getString("400_kv_sc"));
                    dto.setPcost(rs.getString("220_kv_dc"));
                    dto.setInstalledcapacity(rs.getString("220_kv_sc"));
                    dto.setDesignenegry(rs.getString("132_kv_dc"));
                    dto.setFirmpower(rs.getString("132_kv_sc"));
                    dto.setGrosshead(rs.getString("66_kv_dc"));
                    dto.setUnits(rs.getString("66_kv_sc"));
                    dto.setVoltagegen(rs.getString("66_kv_qc"));
                    dto.setVoltagetrans(rs.getString("UG"));
                    dto.setSwitchyard(rs.getString("Remarks"));
                    reportList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException("###Error at AdminDAO[gettariffList]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return reportList;
    }
    
    public static AdminDTO getOpenDeshBord() throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        String query = null;
        final AdminDTO dtlDto = new AdminDTO();
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                query = " SELECT  'Major Hydropower Plants' NAME,  SUM(Installed_Capacity) Y,  'Major' drilldown  FROM  t_hydro_plant_master  UNION  SELECT  'Mini Hydropower Plants' NAME,  SUM(Installed_Capacity / 1000) Y,  'Mini' drilldown  FROM  t_mini_hydroplant_master  UNION  SELECT  'Solar Power Plants' NAME,  SUM(Installed_Capacity / 1000) Y,  'Wind' drilldown  FROM  t_wind_plant_master  UNION  SELECT  'Wind Power Plants' NAME,  SUM(Installed_Capacity / 1000) Y,  'Solar' drilldown  FROM  t_solar_plant_master  UNION  SELECT  'Diesel Generation Plants' NAME,  SUM(Installed_Capacity / 1000) Y,  'Diesel' drilldown  FROM  t_dg_set_master";
                pst = conn.prepareStatement(query);
                rs = pst.executeQuery();
                while (rs.next()) {
                    if (rs.getString("drilldown").equals("Major")) {
                        dtlDto.setInstalCapicityMW(rs.getString("Y"));
                    }
                    else if (rs.getString("drilldown").equals("Mini")) {
                        dtlDto.setInstalCapicityMiniMW(rs.getString("Y"));
                    }
                    else if (rs.getString("drilldown").equals("Wind")) {
                        dtlDto.setInstalCapicityWindMW(rs.getString("Y"));
                    }
                    else if (rs.getString("drilldown").equals("Solar")) {
                        dtlDto.setInstalCapicitySolarMW(rs.getString("Y"));
                    }
                    else {
                        if (!rs.getString("drilldown").equals("Diesel")) {
                            continue;
                        }
                        dtlDto.setInstalCapicityDGMW(rs.getString("Y"));
                    }
                }
            }
        }
        catch (Exception e) {
            System.out.println("####### Error in AdminDAO[getOpenDeshBord]: " + e);
            return dtlDto;
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return dtlDto;
    }
    
    public static AdminDTO getPublicInstalledCapacity() throws HPSException, HPSSystemException, SQLException, ParseException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        String query = null;
        final AdminDTO dtlDto = new AdminDTO();
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                query = "SELECT 'Major Hydro Power Plants  - ' plantName, SUM(Installed_Capacity)  totalCapacity FROM t_hydro_plant_master UNION SELECT 'Mini Hydro Power Plants - ' plantName, SUM(Installed_Capacity/1000) totalCapacity FROM t_mini_hydroplant_master UNION SELECT 'Solar Power Plants - ' plantName, SUM(Installed_Capacity/1000)totalCapacity FROM t_solar_plant_master UNION SELECT 'Wind Power Plants - ' plantName, SUM(Installed_Capacity/1000) totalCapacity FROM t_wind_plant_master UNION SELECT 'DG Power Plants - ' plantName, SUM(Installed_Capacity/1000) totalCapacity FROM t_dg_set_master";
                pst = conn.prepareStatement(query);
                rs = pst.executeQuery();
                while (rs.next()) {
                    dtlDto.setPlantname(rs.getString("plantName"));
                    dtlDto.setInstalCapicityMW(rs.getString("totalCapacity"));
                }
            }
        }
        catch (Exception e) {
            System.out.println("####### Error in AdminDAO[getInstalCapicityMW]: " + e);
            return dtlDto;
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return dtlDto;
    }
    
    public static AdminDTO getPublicMU(final String fromDateGen, final String toDateGen) throws HPSException, HPSSystemException, SQLException, ParseException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        String query = null;
        final AdminDTO dtlDto = new AdminDTO();
        final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
        final java.util.Date date = sdfsource.parse(fromDateGen);
        final java.util.Date date2 = sdfsource.parse(toDateGen);
        final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
        final String Newdate = sdf.format(date);
        final String Newdate2 = sdf.format(date2);
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                query = "SELECT  IF( (FORMAT(SUM(a.`MU`), 2)) IS NULL,  'Empty', FORMAT(SUM(a.`MU`), 2)  ) AS TOTAL_MU  FROM  `t_hourly_data_dgpc2` a  WHERE a.`Record_Date` BETWEEN ? AND ?";
                pst = conn.prepareStatement(query);
                pst.setString(1, Newdate);
                pst.setString(2, Newdate2);
                rs = pst.executeQuery();
                while (rs.next()) {
                    dtlDto.setTotalGenMU(rs.getString("TOTAL_MU"));
                }
            }
        }
        catch (Exception e) {
            System.out.println("####### Error in AdminDAO[getPublicMU]: " + e);
            return dtlDto;
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return dtlDto;
    }
    
    public static AdminDTO getPublicMW(final String fromDateDem) throws HPSException, HPSSystemException, SQLException, ParseException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        String query = null;
        final AdminDTO dtlDto = new AdminDTO();
        final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
        final java.util.Date date = sdfsource.parse(fromDateDem);
        final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
        final String Newdate = sdf.format(date);
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                query = "SELECT Record_hour, SUM(MW) AS peakMW FROM t_hourly_data_bpc WHERE Date_Of_Reading = ? GROUP BY Record_hour HAVING SUM(MW) = (SELECT MAX(peakMW) FROM (SELECT SUM(MW)  peakMW, Record_hour FROM t_hourly_data_bpc WHERE Date_Of_Reading = ? GROUP BY Record_hour) tab)";
                pst = conn.prepareStatement(query);
                pst.setString(1, Newdate);
                pst.setString(2, Newdate);
                rs = pst.executeQuery();
                while (rs.next()) {
                    dtlDto.setHour(rs.getString("Record_hour"));
                    dtlDto.setTaoalDemandMW(rs.getString("peakMW"));
                }
            }
        }
        catch (Exception e) {
            System.out.println("####### Error in AdminDAO[getPublicMW]: " + e);
            return dtlDto;
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return dtlDto;
    }
    
    public AdminDTO getTariffDtls(final String id) throws HPSException, HPSSystemException {
        final AdminDTO dto = new AdminDTO();
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT  a.`Plant_Name`, a.`Tariff`, a.`Tariff_Type`, DATE_FORMAT(a.`Tariff_Set_Date`,'%d/%m/%Y') tariffSetDate, a.`Tariff_Code` FROM `t_tariff_master` a WHERE a.`Tariff_Code` = ?");
                pst.setString(1, id);
                rs = pst.executeQuery();
                while (rs.next()) {
                    dto.setPlantname(rs.getString("Plant_Name"));
                    dto.setTariff(rs.getString("Tariff"));
                    dto.setTariffType(rs.getString("Tariff_Type"));
                    dto.setTariffSetDate(rs.getString("tariffSetDate"));
                    dto.setTariffCode(rs.getString("Tariff_Code"));
                }
            }
        }
        catch (Exception e) {
            throw new HPSException();
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return dto;
    }
    
    public AdminDTO getWheelingDtls(final String id) throws HPSException, HPSSystemException {
        final AdminDTO dto = new AdminDTO();
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT a.`Wheeling`, DATE_FORMAT(a.`Wheeling_Set_Date`,'%d/%m/%Y') WheelingSetDate, a.`Wheeling_Code` FROM `t_wheeling_master` a WHERE a.`Wheeling_Code` = ?");
                pst.setString(1, id);
                rs = pst.executeQuery();
                while (rs.next()) {
                    dto.setWheeling(rs.getString("Wheeling"));
                    dto.setWheelingSetDate(rs.getString("WheelingSetDate"));
                    dto.setWheelingCode(rs.getString("Wheeling_Code"));
                }
            }
        }
        catch (Exception e) {
            throw new HPSException();
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return dto;
    }
    
    public AdminDTO getDgDtls(final String id) throws HPSException, HPSSystemException {
        final AdminDTO dto = new AdminDTO();
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT  `Plant_Name`, `Location`, DATE_FORMAT(a.`Com_Operation_Date`,'%d/%m/%Y') Com_Operation_Date, `Installed_Capacity`, a.`Plant_Code` FROM `t_dg_set_master` a WHERE a.`Plant_Code` = ?");
                pst.setString(1, id);
                rs = pst.executeQuery();
                while (rs.next()) {
                    dto.setPlantname(rs.getString("Plant_Name"));
                    dto.setPlantlocation(rs.getString("Location"));
                    dto.setOperationDate(rs.getString("Com_Operation_Date"));
                    dto.setInstalledcapacity(rs.getString("Installed_Capacity"));
                    dto.setPlantcode(rs.getString("Plant_Code"));
                }
            }
        }
        catch (Exception e) {
            throw new HPSException();
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return dto;
    }
    
    public AdminDTO getHydroPowerDtls(final String id) throws HPSException, HPSSystemException {
        final AdminDTO dto = new AdminDTO();
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT  `Plant_Name`, `Location`, DATE_FORMAT(`Com_Operation_Date`,'%d/%m/%Y') Com_Operation_Date, `DPR_Prepared_By`, `DRP_Cost`, `Project_Completion_Cost`, `Installed_Capacity`, `Design_Energy`, `Units_No`, `Firm_Power`, `Catchment_Area`, `Net_Head`, `Gross_Head`, `Voltage_Gen`, `Voltage_Trans`, `Switch_Yard`, `Gen_Trans_Capacity`, `No_Ckts`, `No_Bays`, `Switch_Yard_Type`, `Discharge`, `Turbine_Type`, `Loan_Financing`, `Grant_equity`, `Tariff`, a.`Plant_Code` FROM `t_hydro_plant_master` a  WHERE a.`Plant_Code` = ?  ");
                pst.setString(1, id);
                rs = pst.executeQuery();
                while (rs.next()) {
                    dto.setPlantname(rs.getString("Plant_Name"));
                    dto.setPlantlocation(rs.getString("Location"));
                    dto.setOperationDate(rs.getString("Com_Operation_Date"));
                    dto.setDrp(rs.getString("DPR_Prepared_By"));
                    dto.setPcost(rs.getString("DRP_Cost"));
                    dto.setComCost(rs.getString("Project_Completion_Cost"));
                    dto.setInstalledcapacity(rs.getString("Installed_Capacity"));
                    dto.setDesignenegry(rs.getString("Design_Energy"));
                    dto.setUnits(rs.getString("Units_No"));
                    dto.setFirmpower(rs.getString("Firm_Power"));
                    dto.setCatchmentarea(rs.getString("Catchment_Area"));
                    dto.setNethead(rs.getString("Net_Head"));
                    dto.setGrosshead(rs.getString("Gross_Head"));
                    dto.setVoltagegen(rs.getString("Voltage_Gen"));
                    dto.setVoltagetrans(rs.getString("Voltage_Trans"));
                    dto.setSwitchyard(rs.getString("Switch_Yard"));
                    dto.setTrancapacity(rs.getString("Gen_Trans_Capacity"));
                    dto.setCkts(rs.getString("No_Ckts"));
                    dto.setBays(rs.getString("No_Bays"));
                    dto.setSwitchyardtype(rs.getString("Switch_Yard_Type"));
                    dto.setDischarge(rs.getString("Discharge"));
                    dto.setTurbine(rs.getString("Turbine_Type"));
                    dto.setLoanfinance(rs.getString("Loan_Financing"));
                    dto.setEquity(rs.getString("Grant_equity"));
                    dto.setTariff(rs.getString("Tariff"));
                    dto.setPlantcode(rs.getString("Plant_Code"));
                }
            }
        }
        catch (Exception e) {
            throw new HPSException();
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return dto;
    }
    
    public AdminDTO getMinihydroPowerDtls(final String id) throws HPSException, HPSSystemException {
        final AdminDTO dto = new AdminDTO();
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT   `Plant_Name`, `Location`, DATE_FORMAT(`Com_Operation_Date`,'%d/%m/%Y') Com_Operation_Date, `Installed_Capacity`, `Design_Energy`, `Units_No`, `Gross_Head`, `Voltage_Generation`, `Voltage_Transmission`, `Gen_Trans_Capacity`, `No_Ckts`, a.`Plant_Code` FROM `t_mini_hydroplant_master` a WHERE a.`Plant_Code` = ? ");
                pst.setString(1, id);
                rs = pst.executeQuery();
                while (rs.next()) {
                    dto.setPlantname(rs.getString("Plant_Name"));
                    dto.setPlantlocation(rs.getString("Location"));
                    dto.setOperationDate(rs.getString("Com_Operation_Date"));
                    dto.setInstalledcapacity(rs.getString("Installed_Capacity"));
                    dto.setDesignenegry(rs.getString("Design_Energy"));
                    dto.setUnits(rs.getString("Units_No"));
                    dto.setGrosshead(rs.getString("Gross_Head"));
                    dto.setVoltagegen(rs.getString("Voltage_Generation"));
                    dto.setVoltagetrans(rs.getString("Voltage_Transmission"));
                    dto.setTrancapacity(rs.getString("Gen_Trans_Capacity"));
                    dto.setCkts(rs.getString("No_Ckts"));
                    dto.setPlantcode(rs.getString("Plant_Code"));
                }
            }
        }
        catch (Exception e) {
            throw new HPSException();
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return dto;
    }
    
    public AdminDTO getWindPowerDtls(final String id) throws HPSException, HPSSystemException {
        final AdminDTO dto = new AdminDTO();
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT  `Plant_Name`, `Location`, DATE_FORMAT(`Com_Operation_Date`,'%d/%m/%Y') Com_Operation_Date, `Installed_Capacity`, `Design_Energy`, `Plant_Code`  FROM `t_wind_plant_master` a WHERE a.`Plant_Code` = ? ");
                pst.setString(1, id);
                rs = pst.executeQuery();
                while (rs.next()) {
                    dto.setPlantname(rs.getString("Plant_Name"));
                    dto.setPlantlocation(rs.getString("Location"));
                    dto.setOperationDate(rs.getString("Com_Operation_Date"));
                    dto.setInstalledcapacity(rs.getString("Installed_Capacity"));
                    dto.setDesignenegry(rs.getString("Design_Energy"));
                    dto.setPlantcode(rs.getString("Plant_Code"));
                }
            }
        }
        catch (Exception e) {
            throw new HPSException();
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return dto;
    }
    
    public AdminDTO getSolarPowerDtls(final String id) throws HPSException, HPSSystemException {
        final AdminDTO dto = new AdminDTO();
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT  `Plant_Name`, `Location`, DATE_FORMAT(`Com_Operation_Date`,'%d/%m/%Y') Com_Operation_Date, `Installed_Capacity`, `Design_Energy`, `Plant_Code` FROM `t_solar_plant_master` a WHERE a.`Plant_Code` = ? ");
                pst.setString(1, id);
                rs = pst.executeQuery();
                while (rs.next()) {
                    dto.setPlantname(rs.getString("Plant_Name"));
                    dto.setPlantlocation(rs.getString("Location"));
                    dto.setOperationDate(rs.getString("Com_Operation_Date"));
                    dto.setInstalledcapacity(rs.getString("Installed_Capacity"));
                    dto.setDesignenegry(rs.getString("Design_Energy"));
                    dto.setPlantcode(rs.getString("Plant_Code"));
                }
            }
        }
        catch (Exception e) {
            throw new HPSException();
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return dto;
    }
    
    public AdminDTO getTransmissionDtls(final String id) throws HPSException, HPSSystemException {
        final AdminDTO dto = new AdminDTO();
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT  `Transmission_Name`, `400_kv_dc`, `400_kv_sc`, `220_kv_dc`, `220_kv_sc`, `132_kv_dc`, `132_kv_sc`, `66_kv_dc`, `66_kv_sc`, `66_kv_qc`, `UG`, `Type_of_Conductor`, `Remarks`, `Transmission_Code` FROM  `t_trasmission_master` a WHERE a.`Transmission_Code` = ? ");
                pst.setString(1, id);
                rs = pst.executeQuery();
                while (rs.next()) {
                    dto.setPlantname(rs.getString("Transmission_Name"));
                    dto.setPlantlocation(rs.getString("400_kv_dc"));
                    dto.setDrp(rs.getString("400_kv_sc"));
                    dto.setPcost(rs.getString("220_kv_dc"));
                    dto.setInstalledcapacity(rs.getString("220_kv_sc"));
                    dto.setDesignenegry(rs.getString("132_kv_dc"));
                    dto.setUnits(rs.getString("132_kv_sc"));
                    dto.setFirmpower(rs.getString("66_kv_dc"));
                    dto.setGrosshead(rs.getString("66_kv_sc"));
                    dto.setVoltagegen(rs.getString("66_kv_qc"));
                    dto.setVoltagetrans(rs.getString("UG"));
                    dto.setTurbine(rs.getString("Type_of_Conductor"));
                    dto.setSwitchyard(rs.getString("Remarks"));
                    dto.setTransmissionCode(rs.getString("Transmission_Code"));
                }
            }
        }
        catch (Exception e) {
            throw new HPSException();
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return dto;
    }
    
    public AdminDTO getSubStationDtls(final String id) throws HPSException, HPSSystemException {
        final AdminDTO dto = new AdminDTO();
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" SELECT  `Substation_Name`, `Location`, DATE_FORMAT(`Com_Operation_Date`,'%d/%m/%Y') Com_Operation_Date, `Capacity`, `Voltage_Ratio`, `Transformer`,  `Area`, `Substation_Code` FROM `t_sub_station_master` a WHERE a.`Substation_Code` = ? ");
                pst.setString(1, id);
                rs = pst.executeQuery();
                while (rs.next()) {
                    dto.setPlantname(rs.getString("Substation_Name"));
                    dto.setPlantlocation(rs.getString("Location"));
                    dto.setOperationDate(rs.getString("Com_Operation_Date"));
                    dto.setInstalledcapacity(rs.getString("Capacity"));
                    dto.setVoltagetrans(rs.getString("Voltage_Ratio"));
                    dto.setTrancapacity(rs.getString("Transformer"));
                    dto.setDesignenegry(rs.getString("Area"));
                    dto.setSubStationCode(rs.getString("Substation_Code"));
                }
            }
        }
        catch (Exception e) {
            throw new HPSException();
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return dto;
    }
    
    public ReportDTO getReportdetails(final ReportFormBean repoFormBean) throws HPSException, HPSSystemException, ParseException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        final ReportDTO dto = new ReportDTO();
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
                final java.util.Date date = sdfsource.parse(repoFormBean.getRecordDate());
                final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
                final String recordDate = sdf.format(date);
                pst = conn.prepareStatement("SELECT a.`Plant_Name`,DATE_FORMAT(a.`Record_Date`,'%d %M %Y') AS RecordDate, a.`Max_Inflow`,a.`Min_Inflow`,a.`Max_Frequency`,a.`Min_Frequency`FROM `t_hourly_data_dgpc1`a WHERE a.`Record_Date`=? AND a.`Plant_Id`=? LIMIT 1");
                pst.setString(1, recordDate);
                pst.setString(2, repoFormBean.getHydroPlantId());
                rs = pst.executeQuery();
                if (rs.first()) {
                    dto.setPlantName(rs.getString("Plant_Name"));
                    dto.setDataDate(rs.getString("RecordDate"));
                    dto.setMaxInFlow(rs.getString("Max_Inflow"));
                    dto.setMinInFlow(rs.getString("Min_Inflow"));
                    dto.setMaxFrequency(rs.getString("Max_Frequency"));
                    dto.setMinFrequency(rs.getString("Min_Frequency"));
                }
            }
        }
        catch (Exception ex) {}
        return dto;
    }
    
    public ReportDTO getSubstationdetails(final ReportFormBean repoFormBean) throws HPSException, HPSSystemException, ParseException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        final ReportDTO dto1 = new ReportDTO();
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
                final java.util.Date date = sdfsource.parse(repoFormBean.getRecordDate());
                final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
                final String recordDate = sdf.format(date);
                pst = conn.prepareStatement("SELECT DATE_FORMAT(b.`Date_Of_Reading`,'%d %M %Y') AS recorddate,b.`Sub_Station_Name` FROM `t_hourly_data_bpc` b WHERE b.`Date_Of_Reading`=? AND b.`Sub_Station_Id`=? ");
                pst.setString(1, recordDate);
                pst.setString(2, repoFormBean.getSubstationId());
                rs = pst.executeQuery();
                if (rs.first()) {
                    dto1.setPlantname(rs.getString("Sub_Station_Name"));
                    dto1.setDataDate(rs.getString("recorddate"));
                }
            }
        }
        catch (Exception ex) {}
        return dto1;
    }
    
    public ReportDTO getWindpowerdetails(final ReportFormBean repoFormBean) throws HPSException, HPSSystemException, ParseException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        final ReportDTO dto2 = new ReportDTO();
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement("SELECT a.`Month`, CASE a.`Month`WHEN '1' THEN 'January'WHEN '2' THEN 'February'WHEN '3' THEN 'March'WHEN '4' THEN 'April'WHEN '4' THEN 'May'WHEN '6' THEN 'June'WHEN '7' THEN 'July'WHEN '8' THEN 'August'WHEN '9' THEN 'September'WHEN '10' THEN 'October'WHEN '11' THEN 'November'WHEN '12' THEN 'December'END AS dmont,a.`Year` FROM `t_monthly_wind_power` a WHERE a.`Month`=? AND a.`Year`=?");
                pst.setString(1, repoFormBean.getMonth());
                pst.setString(2, repoFormBean.getYear());
                rs = pst.executeQuery();
                if (rs.first()) {
                    dto2.setMonth(rs.getString("dmont"));
                    dto2.setYear(rs.getString("Year"));
                }
            }
        }
        catch (Exception ex) {}
        return dto2;
    }
    
    public ReportDTO getMinihydrodetails(final ReportFormBean repoFormBean) throws HPSException, HPSSystemException, ParseException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        final ReportDTO dto3 = new ReportDTO();
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement("SELECT a.`Month`, CASE a.`Month`WHEN '1' THEN 'January'WHEN '2' THEN 'February'WHEN '3' THEN 'March'WHEN '4' THEN 'April'WHEN '4' THEN 'May'WHEN '6' THEN 'June'WHEN '7' THEN 'July'WHEN '8' THEN 'August'WHEN '9' THEN 'September'WHEN '10' THEN 'October'WHEN '11' THEN 'November'WHEN '12' THEN 'December'END AS dmont,a.`Year` FROM `t_monthly_mini_hydro` a WHERE a.`Month`=? AND a.`Year`=?");
                pst.setString(1, repoFormBean.getMonth());
                pst.setString(2, repoFormBean.getYear());
                rs = pst.executeQuery();
                if (rs.first()) {
                    dto3.setMonth(rs.getString("dmont"));
                    dto3.setYear(rs.getString("Year"));
                }
            }
        }
        catch (Exception ex) {}
        return dto3;
    }
    
    public List<ReportDTO> getGeneratReportList(final ReportFormBean repoFormBean) throws HPSException, HPSSystemException, ParseException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        final List<ReportDTO> reportList = new ArrayList<ReportDTO>();
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                if (repoFormBean.getReportId().equalsIgnoreCase("1")) {
                    final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
                    final java.util.Date date = sdfsource.parse(repoFormBean.getRecordDate());
                    final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
                    final String recordDate = sdf.format(date);
                    pst = conn.prepareStatement("SELECT a.`Unit_name`,a.`Record_hour`,a.`MW`,a.`MU`,a.`MVAR`,a.`PF`, a.`Remarks` FROM `t_hourly_data_dgpc2` a LEFT JOIN `t_hourly_data_dgpc1` b ON a.`PRecord_Id`=b.`Record_Id` WHERE b.`Record_Date`=? AND  b.`Plant_Id`=?");
                    pst.setString(1, recordDate);
                    pst.setString(2, repoFormBean.getHydroPlantId());
                    rs = pst.executeQuery();
                    while (rs.next()) {
                        final ReportDTO dto = new ReportDTO();
                        dto.setUnits(rs.getString("Unit_Name"));
                        dto.setDataHour(rs.getString("Record_hour"));
                        dto.setDataMW(rs.getString("MW"));
                        dto.setDataMU(rs.getString("MU"));
                        dto.setDataMVAR(rs.getString("MVAR"));
                        dto.setDataPF(rs.getString("PF"));
                        dto.setDataRemarks(rs.getString("Remarks"));
                        reportList.add(dto);
                    }
                }
                else if (repoFormBean.getReportId().equalsIgnoreCase("2")) {
                    final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
                    final java.util.Date date = sdfsource.parse(repoFormBean.getRecordDate());
                    final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
                    final String recordDate = sdf.format(date);
                    pst = conn.prepareStatement("SELECT a.`Record_hour`,a.`MW`,a.`MVAR`,ROUND((a.`MW` / (b.`capacity` / .9)),2)AS LF FROM `t_hourly_data_bpc` a LEFT JOIN `t_sub_station_master` b ON a.`Sub_Station_Id` = b.`Substation_Code` WHERE a.`Date_Of_Reading` =? AND b.`Substation_Code`=?");
                    pst.setString(1, recordDate);
                    pst.setString(2, repoFormBean.getSubstationId());
                    rs = pst.executeQuery();
                    while (rs.next()) {
                        final ReportDTO dto = new ReportDTO();
                        dto.setDataHour(rs.getString("Record_hour"));
                        dto.setDataMW(rs.getString("MW"));
                        dto.setDataMVAR(rs.getString("MVAR"));
                        dto.setDataLF(rs.getString("LF"));
                        reportList.add(dto);
                    }
                }
                else if (repoFormBean.getReportId().equalsIgnoreCase("3")) {
                    pst = conn.prepareStatement("SELECT a.`Plant_Name`,a.`MU`,a.`MW`  FROM `t_monthly_mini_hydro` a WHERE a.`Month`=? AND a.`Year`=?");
                    pst.setString(1, repoFormBean.getMonth());
                    pst.setString(2, repoFormBean.getYear());
                    rs = pst.executeQuery();
                    while (rs.next()) {
                        final ReportDTO dto = new ReportDTO();
                        dto.setPlantname(rs.getString("Plant_Name"));
                        dto.setDataMU(rs.getString("MU"));
                        dto.setDataMW(rs.getString("MW"));
                        reportList.add(dto);
                    }
                }
                else if (repoFormBean.getReportId().equalsIgnoreCase("4")) {
                    pst = conn.prepareStatement("SELECT a.`Plant_Name`,a.`Day`,a.`T1_Energy_Generated`,a.`T2_Energy_Generated`,a.`Total_Energy_Generated`,a.`T1_Machine_Availability(hrs)`,a.`T2_Machine_Availability(hrs)` FROM `t_monthly_wind_power` a WHERE a.`Month`=? AND a.`Year`=?");
                    pst.setString(1, repoFormBean.getMonth());
                    pst.setString(2, repoFormBean.getYear());
                    rs = pst.executeQuery();
                    while (rs.next()) {
                        final ReportDTO dto = new ReportDTO();
                        dto.setPlantname(rs.getString("Plant_Name"));
                        dto.setDay(rs.getString("Day"));
                        dto.setT1energy(rs.getString("T1_Energy_Generated"));
                        dto.setT2energy(rs.getString("T2_Energy_Generated"));
                        dto.setTotal(rs.getString("Total_Energy_Generated"));
                        dto.setT1available(rs.getString("T1_Machine_Availability(hrs)"));
                        dto.setT2available(rs.getString("T2_Machine_Availability(hrs)"));
                        reportList.add(dto);
                    }
                }
                else if (repoFormBean.getReportId().equalsIgnoreCase("5")) {
                    pst = conn.prepareStatement("SELECT a.`Transmission_Name`, a.`400_kv_dc`,a.`400_kv_sc`,a.`220_kv_dc`,a.`220_kv_sc`,a.`132_kv_dc`,a.`132_kv_sc`,a.`66_kv_dc`,a.`66_kv_sc`,a.`66_kv_qc`,a.`UG`,a.`Remarks` FROM `t_trasmission_master`a ");
                    rs = pst.executeQuery();
                    while (rs.next()) {
                        final ReportDTO dto = new ReportDTO();
                        dto.setPlantname(rs.getString("Transmission_Name"));
                        dto.setPlantlocation(rs.getString("400_kv_dc"));
                        dto.setDrp(rs.getString("400_kv_sc"));
                        dto.setPcost(rs.getString("220_kv_dc"));
                        dto.setInstalledcapacity(rs.getString("220_kv_sc"));
                        dto.setDesignenegry(rs.getString("132_kv_dc"));
                        dto.setFirmpower(rs.getString("132_kv_sc"));
                        dto.setGrosshead(rs.getString("66_kv_dc"));
                        dto.setUnits(rs.getString("66_kv_sc"));
                        dto.setVoltagegen(rs.getString("66_kv_qc"));
                        dto.setVoltagetrans(rs.getString("UG"));
                        dto.setSwitchyard(rs.getString("Remarks"));
                        reportList.add(dto);
                    }
                }
                else if (repoFormBean.getReportId().equalsIgnoreCase("6")) {
                    final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
                    final java.util.Date fdate = sdfsource.parse(repoFormBean.getFromDate());
                    final java.util.Date tdate = sdfsource.parse(repoFormBean.getToDate());
                    final SimpleDateFormat sdf2 = new SimpleDateFormat("yyyy-mm-dd");
                    final String fromDate = sdf2.format(fdate);
                    final String toDate = sdf2.format(tdate);
                    pst = conn.prepareStatement("SELECT a.`Plant_Id`,a.`Plant_Name`,SUM(b.`MU`) AS MU FROM `t_hourly_data_dgpc1` a LEFT JOIN `t_hourly_data_dgpc2`b ON a.`Record_Id`=b.`PRecord_Id` WHERE a.`Record_Date` BETWEEN ? AND ? GROUP BY a.`Plant_Id`");
                    pst.setString(1, fromDate);
                    pst.setString(2, toDate);
                    rs = pst.executeQuery();
                    while (rs.next()) {
                        final ReportDTO dto = new ReportDTO();
                        dto.setHydroPlantId(rs.getString("Plant_Id"));
                        dto.setPlantName(rs.getString("Plant_Name"));
                        dto.setDataMU(rs.getString("MU"));
                        reportList.add(dto);
                    }
                }
                else if (repoFormBean.getReportId().equalsIgnoreCase("7")) {
                    if (repoFormBean.getDzongkhagId().equalsIgnoreCase("All") && repoFormBean.getMonth().equalsIgnoreCase("All")) {
                        pst = conn.prepareStatement("SELECT t.Data_Year, ROUND(((Total_Low_Vol_Ru/Grand_Total)*100),2) LVRpercent , \t\t      ROUND(((Total_Low_Vol_Ru_Coo/Grand_Total)*100),2)  Ru_Coo_percent, \t\t      ROUND(((Total_Low_Vol_Ru_MT/Grand_Total)*100) ,2) Ru_MT_percent, \t\t      ROUND(((Total_Low_Vol_Ru_CL/Grand_Total)*100),2)  Ru_CL_percent, \t\t      ROUND(((Total_Low_Vol_Urban /Grand_Total)*100),2)  Urban_percent, \t\t      ROUND(((Total_Low_Vol_RI /Grand_Total)*100),2)  RI_percent, \t\t      ROUND(((Low_Vol_B3_Com/Grand_Total)*100),2) Com_percent, \t\t      ROUND(((Low_Vol_B3_Ind/Grand_Total)*100),2) Ind_percent, \t\t      ROUND(((Low_Vol_B3_Agr/Grand_Total)*100),2) Agr_percent, \t\t      ROUND(((Low_Vol_B3_Ins/Grand_Total)*100),2) Ins_percent, \t\t      ROUND(((Low_Vol_B3_SL/Grand_Total)*100),2) SL_percent, \t\t      ROUND(((Low_Vol_B3_PHA/Grand_Total)*100),2) PHA_percent, \t\t      ROUND(((Low_Vol_B3_TC /Grand_Total)*100),2) TC_percent, \t\t      ROUND(((LV_Bulk_B3/Grand_Total)*100),2) LV_Bulk_percent, \t\t      ROUND(((Med_Vol_B3/Grand_Total)*100),2) Med_Vol_B3_percent, \t\t      ROUND(((High_Vol_B3 /Grand_Total)*100),2) High_Vol_B3_percent, \t\t      Total_Low_Vol_Ru, \t\t      Total_Low_Vol_Ru_Coo, \t\t      Total_Low_Vol_Ru_MT, \t\t      Total_Low_Vol_Ru_CL, \t\t      Total_Low_Vol_Urban , \t\t      Total_Low_Vol_RI, \t\t      Low_Vol_B3_Com , \t\t      Low_Vol_B3_Ind , \t\t      Low_Vol_B3_Agr , \t\t      Low_Vol_B3_Ins , \t\t      Low_Vol_B3_SL , \t\t      Low_Vol_B3_PHA , \t\t      Low_Vol_B3_TC , \t\t      LV_Bulk_B3 , \t\t      Med_Vol_B3 , \t\t      High_Vol_B3 , \t\t      Grand_Total \t\t       FROM (SELECT a.Data_Year,(SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) )AS Total_Low_Vol_Ru, \t\t \t\t(SUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)) AS Total_Low_Vol_Ru_Coo , \t\t        (SUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT))AS Total_Low_Vol_Ru_MT , \t\t\t\t(SUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL ))AS Total_Low_Vol_Ru_CL , \t\t \t\t(SUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)) AS Total_Low_Vol_Urban , \t\t\t\t(SUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) )AS Total_Low_Vol_RI , \t\t\t\tSUM(Low_Vol_B3_Com)AS Low_Vol_B3_Com , \t\t\t\tSUM(Low_Vol_B3_Ind)AS Low_Vol_B3_Ind , \t\t\t\tSUM(Low_Vol_B3_Agr) AS Low_Vol_B3_Agr , \t\t\t\tSUM(Low_Vol_B3_Ins)AS Low_Vol_B3_Ins , \t\t\t\tSUM(Low_Vol_B3_SL)AS Low_Vol_B3_SL , \t\t \t\tSUM(Low_Vol_B3_PHA) AS Low_Vol_B3_PHA , \t\t\t    SUM(Low_Vol_B3_TC)AS Low_Vol_B3_TC , \t\t  \t\tSUM(LV_Bulk_B3)AS LV_Bulk_B3 , \t\t \t\tSUM(Med_Vol_B3)AS Med_Vol_B3 , \t\t \t\tSUM(High_Vol_B3) AS High_Vol_B3 , \t\t\t    (SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) + \t\t\t\tSUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)+ \t\t \t\tSUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT)+ \t\t\t\tSUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL )+ \t\t \t\tSUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)+ \t\t\t\tSUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) + \t\t  \t\tSUM(Low_Vol_B3_Com)+ \t\t \t\tSUM(Low_Vol_B3_Ind)+ \t\t  \t\tSUM(Low_Vol_B3_Agr)+ \t\t \t\tSUM(Low_Vol_B3_Ins)+ \t\t \t\tSUM(Low_Vol_B3_SL)+ \t\t\t\tSUM(Low_Vol_B3_PHA)+ \t\t \t\tSUM(Low_Vol_B3_TC)+ \t\t\t    SUM(LV_Bulk_B3)+ \t\t\t\tSUM(Med_Vol_B3)+ \t\t\t    SUM(High_Vol_B3)) AS Grand_Total \t\t \t\tFROM `t_bpc_energy_utilization_dzongkhag_wise2` a \t\t\t\tWHERE a.`Data_Year`=?) t;");
                        pst.setString(1, repoFormBean.getYear());
                    }
                    else if (repoFormBean.getDzongkhagId().equalsIgnoreCase("All")) {
                        pst = conn.prepareStatement("SELECT t.Data_Year,ROUND(((Total_Low_Vol_Ru/Grand_Total)*100),2) LVRpercent , \t      ROUND(((Total_Low_Vol_Ru_Coo/Grand_Total)*100),2)  Ru_Coo_percent, \t      ROUND(((Total_Low_Vol_Ru_MT/Grand_Total)*100) ,2) Ru_MT_percent, \t      ROUND(((Total_Low_Vol_Ru_CL/Grand_Total)*100),2)  Ru_CL_percent, \t      ROUND(((Total_Low_Vol_Urban /Grand_Total)*100),2)  Urban_percent, \t      ROUND(((Total_Low_Vol_RI /Grand_Total)*100),2)  RI_percent, \t      ROUND(((Low_Vol_B3_Com/Grand_Total)*100),2) Com_percent, \t      ROUND(((Low_Vol_B3_Ind/Grand_Total)*100),2) Ind_percent, \t      ROUND(((Low_Vol_B3_Agr/Grand_Total)*100),2) Agr_percent, \t      ROUND(((Low_Vol_B3_Ins/Grand_Total)*100),2) Ins_percent, \t      ROUND(((Low_Vol_B3_SL/Grand_Total)*100),2) SL_percent, \t      ROUND(((Low_Vol_B3_PHA/Grand_Total)*100),2) PHA_percent, \t      ROUND(((Low_Vol_B3_TC /Grand_Total)*100),2) TC_percent, \t      ROUND(((LV_Bulk_B3/Grand_Total)*100),2) LV_Bulk_percent, \t      ROUND(((Med_Vol_B3/Grand_Total)*100),2) Med_Vol_B3_percent, \t      ROUND(((High_Vol_B3 /Grand_Total)*100),2) High_Vol_B3_percent, \t      Total_Low_Vol_Ru, \t      Total_Low_Vol_Ru_Coo, \t      Total_Low_Vol_Ru_MT, \t      Total_Low_Vol_Ru_CL, \t      Total_Low_Vol_Urban , \t      Total_Low_Vol_RI, \t      Low_Vol_B3_Com , \t      Low_Vol_B3_Ind , \t      Low_Vol_B3_Agr , \t      Low_Vol_B3_Ins , \t      Low_Vol_B3_SL , \t      Low_Vol_B3_PHA , \t      Low_Vol_B3_TC , \t      LV_Bulk_B3 , \t      Med_Vol_B3 , \t      High_Vol_B3 , \t      Grand_Total \t     FROM (SELECT a.Data_Year,(SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) )AS Total_Low_Vol_Ru, \t\t \t\t(SUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)) AS Total_Low_Vol_Ru_Coo , \t\t  \t\t(SUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT))AS Total_Low_Vol_Ru_MT , \t\t\t\t(SUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL ))AS Total_Low_Vol_Ru_CL , \t\t  \t\t(SUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)) AS Total_Low_Vol_Urban , \t\t \t\t(SUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) )AS Total_Low_Vol_RI , \t\t\t\tSUM(Low_Vol_B3_Com)AS Low_Vol_B3_Com , \t\t \t\tSUM(Low_Vol_B3_Ind)AS Low_Vol_B3_Ind , \t\t \t\tSUM(Low_Vol_B3_Agr) AS Low_Vol_B3_Agr , \t\t\t\tSUM(Low_Vol_B3_Ins)AS Low_Vol_B3_Ins , \t\t  \t\tSUM(Low_Vol_B3_SL)AS Low_Vol_B3_SL , \t\t \t\tSUM(Low_Vol_B3_PHA) AS Low_Vol_B3_PHA , \t\t \t\tSUM(Low_Vol_B3_TC)AS Low_Vol_B3_TC , \t\t  \t\tSUM(LV_Bulk_B3)AS LV_Bulk_B3 , \t\t  \t\tSUM(Med_Vol_B3)AS Med_Vol_B3 , \t\t  \t\tSUM(High_Vol_B3) AS High_Vol_B3 , \t\t \t    (SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) + \t\t \t\tSUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)+ \t\t\t\tSUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT)+ \t\t \t\tSUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL )+ \t\t  \t\tSUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)+ \t\t  \t\tSUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) + \t\t  \t\tSUM(Low_Vol_B3_Com)+ \t\t  \t\tSUM(Low_Vol_B3_Ind)+ \t\t  \t\tSUM(Low_Vol_B3_Agr)+ \t\t  \t\tSUM(Low_Vol_B3_Ins)+ \t\t  \t\tSUM(Low_Vol_B3_SL)+ \t\t \t\tSUM(Low_Vol_B3_PHA)+ \t\t  \t\tSUM(Low_Vol_B3_TC)+ \t\t  \t\tSUM(LV_Bulk_B3)+ \t\t  \t\tSUM(Med_Vol_B3)+ \t\t \t\tSUM(High_Vol_B3)) AS Grand_Total \t\t \t\tFROM `t_bpc_energy_utilization_dzongkhag_wise2` a \t\t  \t\tWHERE a.`Data_Month`=? AND a.`Data_Year`=?) t;");
                        pst.setString(1, repoFormBean.getMonth());
                        pst.setString(2, repoFormBean.getYear());
                    }
                    else if (repoFormBean.getMonth().equalsIgnoreCase("All")) {
                        pst = conn.prepareStatement(" SELECT t.Data_Year, ROUND(((Total_Low_Vol_Ru/Grand_Total)*100),2) LVRpercent ,        ROUND(((Total_Low_Vol_Ru_Coo/Grand_Total)*100),2)  Ru_Coo_percent,        ROUND(((Total_Low_Vol_Ru_MT/Grand_Total)*100) ,2) Ru_MT_percent,        ROUND(((Total_Low_Vol_Ru_CL/Grand_Total)*100),2)  Ru_CL_percent,        ROUND(((Total_Low_Vol_Urban /Grand_Total)*100),2)  Urban_percent,        ROUND(((Total_Low_Vol_RI /Grand_Total)*100),2)  RI_percent,        ROUND(((Low_Vol_B3_Com/Grand_Total)*100),2) Com_percent,        ROUND(((Low_Vol_B3_Ind/Grand_Total)*100),2) Ind_percent,        ROUND(((Low_Vol_B3_Agr/Grand_Total)*100),2) Agr_percent,        ROUND(((Low_Vol_B3_Ins/Grand_Total)*100),2) Ins_percent,        ROUND(((Low_Vol_B3_SL/Grand_Total)*100),2) SL_percent,        ROUND(((Low_Vol_B3_PHA/Grand_Total)*100),2) PHA_percent,        ROUND(((Low_Vol_B3_TC /Grand_Total)*100),2) TC_percent,        ROUND(((LV_Bulk_B3/Grand_Total)*100),2) LV_Bulk_percent,        ROUND(((Med_Vol_B3/Grand_Total)*100),2) Med_Vol_B3_percent,        ROUND(((High_Vol_B3 /Grand_Total)*100),2) High_Vol_B3_percent,        Total_Low_Vol_Ru,        Total_Low_Vol_Ru_Coo,        Total_Low_Vol_Ru_MT,        Total_Low_Vol_Ru_CL,        Total_Low_Vol_Urban ,        Total_Low_Vol_RI,        Low_Vol_B3_Com ,        Low_Vol_B3_Ind ,        Low_Vol_B3_Agr ,        Low_Vol_B3_Ins ,        Low_Vol_B3_SL ,        Low_Vol_B3_PHA ,        Low_Vol_B3_TC ,        LV_Bulk_B3 ,        Med_Vol_B3 ,        High_Vol_B3 ,        Grand_Total       FROM (SELECT a.Data_Year,(SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) )AS Total_Low_Vol_Ru, \t\t(SUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)) AS Total_Low_Vol_Ru_Coo , \t\t(SUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT))AS Total_Low_Vol_Ru_MT , \t\t(SUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL ))AS Total_Low_Vol_Ru_CL , \t\t(SUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)) AS Total_Low_Vol_Urban , \t\t(SUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) )AS Total_Low_Vol_RI , \t\tSUM(Low_Vol_B3_Com)AS Low_Vol_B3_Com , \t\tSUM(Low_Vol_B3_Ind)AS Low_Vol_B3_Ind , \t\tSUM(Low_Vol_B3_Agr) AS Low_Vol_B3_Agr , \t\tSUM(Low_Vol_B3_Ins)AS Low_Vol_B3_Ins , \t\tSUM(Low_Vol_B3_SL)AS Low_Vol_B3_SL , \t\tSUM(Low_Vol_B3_PHA) AS Low_Vol_B3_PHA , \t\tSUM(Low_Vol_B3_TC)AS Low_Vol_B3_TC , \t\tSUM(LV_Bulk_B3)AS LV_Bulk_B3 , \t\tSUM(Med_Vol_B3)AS Med_Vol_B3 , \t\tSUM(High_Vol_B3) AS High_Vol_B3 , \t    (SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) + \t\tSUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)+ \t\tSUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT)+ \t\tSUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL )+ \t\tSUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)+ \t\tSUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) + \t\tSUM(Low_Vol_B3_Com)+ \t\tSUM(Low_Vol_B3_Ind)+ \t\tSUM(Low_Vol_B3_Agr)+ \t\tSUM(Low_Vol_B3_Ins)+ \t\tSUM(Low_Vol_B3_SL)+ \t\tSUM(Low_Vol_B3_PHA)+ \t\tSUM(Low_Vol_B3_TC)+ \t\tSUM(LV_Bulk_B3)+ \t\tSUM(Med_Vol_B3)+ \t\tSUM(High_Vol_B3)) AS Grand_Total \t\tFROM `t_bpc_energy_utilization_dzongkhag_wise2` a \t\tWHERE a.`Dzongkhag_Id`=? AND a.`Data_Year`=?) t");
                        pst.setString(1, repoFormBean.getDzongkhagId());
                        pst.setString(2, repoFormBean.getYear());
                    }
                    else {
                        pst = conn.prepareStatement("SELECT  t.Data_Year,ROUND(((Total_Low_Vol_Ru/Grand_Total)*100),2) LVRpercent ,        ROUND(((Total_Low_Vol_Ru_Coo/Grand_Total)*100),2)  Ru_Coo_percent,        ROUND(((Total_Low_Vol_Ru_MT/Grand_Total)*100) ,2) Ru_MT_percent,        ROUND(((Total_Low_Vol_Ru_CL/Grand_Total)*100),2)  Ru_CL_percent,        ROUND(((Total_Low_Vol_Urban /Grand_Total)*100),2)  Urban_percent,        ROUND(((Total_Low_Vol_RI /Grand_Total)*100),2)  RI_percent,        ROUND(((Low_Vol_B3_Com/Grand_Total)*100),2) Com_percent,        ROUND(((Low_Vol_B3_Ind/Grand_Total)*100),2) Ind_percent,        ROUND(((Low_Vol_B3_Agr/Grand_Total)*100),2) Agr_percent,        ROUND(((Low_Vol_B3_Ins/Grand_Total)*100),2) Ins_percent,        ROUND(((Low_Vol_B3_SL/Grand_Total)*100),2) SL_percent,        ROUND(((Low_Vol_B3_PHA/Grand_Total)*100),2) PHA_percent,        ROUND(((Low_Vol_B3_TC /Grand_Total)*100),2) TC_percent,        ROUND(((LV_Bulk_B3/Grand_Total)*100),2) LV_Bulk_percent,        ROUND(((Med_Vol_B3/Grand_Total)*100),2) Med_Vol_B3_percent,        ROUND(((High_Vol_B3 /Grand_Total)*100),2) High_Vol_B3_percent,        Total_Low_Vol_Ru,        Total_Low_Vol_Ru_Coo,        Total_Low_Vol_Ru_MT,        Total_Low_Vol_Ru_CL,        Total_Low_Vol_Urban ,        Total_Low_Vol_RI,        Low_Vol_B3_Com ,        Low_Vol_B3_Ind ,        Low_Vol_B3_Agr ,        Low_Vol_B3_Ins ,        Low_Vol_B3_SL ,        Low_Vol_B3_PHA ,        Low_Vol_B3_TC ,        LV_Bulk_B3 ,        Med_Vol_B3 ,        High_Vol_B3 ,        Grand_Total       FROM (SELECT a.Data_Year,(SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) )AS Total_Low_Vol_Ru, \t\t(SUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)) AS Total_Low_Vol_Ru_Coo , \t\t(SUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT))AS Total_Low_Vol_Ru_MT , \t\t(SUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL ))AS Total_Low_Vol_Ru_CL , \t\t(SUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)) AS Total_Low_Vol_Urban , \t\t(SUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) )AS Total_Low_Vol_RI , \t\tSUM(Low_Vol_B3_Com)AS Low_Vol_B3_Com , \t\tSUM(Low_Vol_B3_Ind)AS Low_Vol_B3_Ind , \t\tSUM(Low_Vol_B3_Agr) AS Low_Vol_B3_Agr , \t\tSUM(Low_Vol_B3_Ins)AS Low_Vol_B3_Ins , \t\tSUM(Low_Vol_B3_SL)AS Low_Vol_B3_SL , \t\tSUM(Low_Vol_B3_PHA) AS Low_Vol_B3_PHA , \t\tSUM(Low_Vol_B3_TC)AS Low_Vol_B3_TC , \t\tSUM(LV_Bulk_B3)AS LV_Bulk_B3 , \t\tSUM(Med_Vol_B3)AS Med_Vol_B3 , \t\tSUM(High_Vol_B3) AS High_Vol_B3 , \t    (SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) + \t\tSUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)+ \t\tSUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT)+ \t\tSUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL )+ \t\tSUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)+ \t\tSUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) + \t\tSUM(Low_Vol_B3_Com)+ \t\tSUM(Low_Vol_B3_Ind)+ \t\tSUM(Low_Vol_B3_Agr)+ \t\tSUM(Low_Vol_B3_Ins)+ \t\tSUM(Low_Vol_B3_SL)+ \t\tSUM(Low_Vol_B3_PHA)+ \t\tSUM(Low_Vol_B3_TC)+ \t\tSUM(LV_Bulk_B3)+ \t\tSUM(Med_Vol_B3)+ \t\tSUM(High_Vol_B3)) AS Grand_Total \t\tFROM `t_bpc_energy_utilization_dzongkhag_wise2` a \t\tWHERE a.`Dzongkhag_Id`=? AND a.`Data_Month`=? AND a.`Data_Year`=?) t");
                        pst.setString(1, repoFormBean.getDzongkhagId());
                        pst.setString(2, repoFormBean.getMonth());
                        pst.setString(3, repoFormBean.getYear());
                    }
                    rs = pst.executeQuery();
                    while (rs.next()) {
                        final ReportDTO dto = new ReportDTO();
                        dto.setYear(rs.getString("Data_Year"));
                        dto.setRrpercentage(rs.getString("LVRpercent"));
                        dto.setRcpercentage(rs.getString("Ru_Coo_percent"));
                        dto.setRmtpercentage(rs.getString("Ru_MT_percent"));
                        dto.setRclpercentage(rs.getString("Ru_CL_percent"));
                        dto.setUpercentage(rs.getString("Urban_percent"));
                        dto.setRipercentage(rs.getString("RI_percent"));
                        dto.setCpercentage(rs.getString("Com_percent"));
                        dto.setIpercentage(rs.getString("Ind_percent"));
                        dto.setApercentage(rs.getString("Agr_percent"));
                        dto.setInspercentage(rs.getString("Ins_percent"));
                        dto.setSlpercentage(rs.getString("SL_percent"));
                        dto.setPhapercentage(rs.getString("PHA_percent"));
                        dto.setTcpercentage(rs.getString("TC_percent"));
                        dto.setLvbpercentage(rs.getString("LV_Bulk_percent"));
                        dto.setMvcpercentage(rs.getString("Med_Vol_B3_percent"));
                        dto.setHvcpercentage(rs.getString("High_Vol_B3_percent"));
                        dto.setRrenergysoldmu(rs.getString("Total_Low_Vol_Ru"));
                        dto.setRcenergysoldmu(rs.getString("Total_Low_Vol_Ru_Coo"));
                        dto.setRmtenergysoldmu(rs.getString("Total_Low_Vol_Ru_MT"));
                        dto.setRclenergysoldmu(rs.getString("Total_Low_Vol_Ru_CL"));
                        dto.setUcenergysoldmu(rs.getString("Total_Low_Vol_Urban"));
                        dto.setRicenergysoldmu(rs.getString("Total_Low_Vol_RI"));
                        dto.setCenergysoldmu(rs.getString("Low_Vol_B3_Com"));
                        dto.setIenergysoldmu(rs.getString("Low_Vol_B3_Ind"));
                        dto.setAenergysoldmu(rs.getString("Low_Vol_B3_Agr"));
                        dto.setInsenergysoldmu(rs.getString("Low_Vol_B3_Ins"));
                        dto.setSlenergysoldmu(rs.getString("Low_Vol_B3_SL"));
                        dto.setPhaenergysoldmu(rs.getString("Low_Vol_B3_SL"));
                        dto.setTcenergysoldmu(rs.getString("Low_Vol_B3_TC"));
                        dto.setLvbenergysoldmu(rs.getString("LV_Bulk_B3"));
                        dto.setMvcenergysoldmu(rs.getString("Med_Vol_B3"));
                        dto.setHvcenergysoldmu(rs.getString("High_Vol_B3"));
                        dto.setTotalsoldmu(rs.getString("Grand_Total"));
                        reportList.add(dto);
                    }
                }
                else if (repoFormBean.getReportId().equalsIgnoreCase("8")) {
                    if (repoFormBean.getDzongkhagId().equalsIgnoreCase("all")) {
                        pst = conn.prepareStatement("SELECT t.Data_Year,ROUND(((Total_Low_Vol_Ru/Grand_Total)*100),2) LVRpercent , ROUND(((Total_Low_Vol_Ru_Coo/Grand_Total)*100),2)  Ru_Coo_percent, ROUND(((Total_Low_Vol_Ru_MT/Grand_Total)*100) ,2) Ru_MT_percent, ROUND(((Total_Low_Vol_Ru_CL/Grand_Total)*100),2)  Ru_CL_percent, ROUND(((Total_Low_Vol_Urban /Grand_Total)*100),2)  Urban_percent, ROUND(((Total_Low_Vol_RI /Grand_Total)*100),2)  RI_percent, ROUND(((Low_Vol_B3_Com/Grand_Total)*100),2) Com_percent, ROUND(((Low_Vol_B3_Ind/Grand_Total)*100),2) Ind_percent, ROUND(((Low_Vol_B3_Agr/Grand_Total)*100),2) Agr_percent, ROUND(((Low_Vol_B3_Ins/Grand_Total)*100),2) Ins_percent, ROUND(((Low_Vol_B3_SL/Grand_Total)*100),2) SL_percent, ROUND(((Low_Vol_B3_PHA/Grand_Total)*100),2) PHA_percent, ROUND(((Low_Vol_B3_TC /Grand_Total)*100),2) TC_percent, ROUND(((LV_Bulk_B3/Grand_Total)*100),2) LV_Bulk_percent, ROUND(((Med_Vol_B3/Grand_Total)*100),2) Med_Vol_B3_percent, ROUND(((High_Vol_B3 /Grand_Total)*100),2) High_Vol_B3_percent, Total_Low_Vol_Ru, Total_Low_Vol_Ru_Coo, Total_Low_Vol_Ru_MT, Total_Low_Vol_Ru_CL, Total_Low_Vol_Urban , Total_Low_Vol_RI, Low_Vol_B3_Com , Low_Vol_B3_Ind , Low_Vol_B3_Agr , Low_Vol_B3_Ins , Low_Vol_B3_SL , Low_Vol_B3_PHA , Low_Vol_B3_TC , LV_Bulk_B3 , Med_Vol_B3 , High_Vol_B3 , Grand_Total FROM (SELECT a.Data_Year,(SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) )AS Total_Low_Vol_Ru, (SUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)) AS Total_Low_Vol_Ru_Coo , (SUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT))AS Total_Low_Vol_Ru_MT , (SUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL ))AS Total_Low_Vol_Ru_CL , (SUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)) AS Total_Low_Vol_Urban , (SUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) )AS Total_Low_Vol_RI , SUM(Low_Vol_B3_Com)AS Low_Vol_B3_Com , SUM(Low_Vol_B3_Ind)AS Low_Vol_B3_Ind , SUM(Low_Vol_B3_Agr) AS Low_Vol_B3_Agr , SUM(Low_Vol_B3_Ins)AS Low_Vol_B3_Ins , SUM(Low_Vol_B3_SL)AS Low_Vol_B3_SL , SUM(Low_Vol_B3_PHA) AS Low_Vol_B3_PHA , SUM(Low_Vol_B3_TC)AS Low_Vol_B3_TC , SUM(LV_Bulk_B3)AS LV_Bulk_B3 , SUM(Med_Vol_B3)AS Med_Vol_B3 , SUM(High_Vol_B3) AS High_Vol_B3 , (SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) + SUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo) + SUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT) + SUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL )+ SUM(Low_Vol_B1_Urban)  +SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban) + SUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI)  + SUM(Low_Vol_B3_Com) + SUM(Low_Vol_B3_Ind) + SUM(Low_Vol_B3_Agr) + SUM(Low_Vol_B3_Ins) + SUM(Low_Vol_B3_SL) + SUM(Low_Vol_B3_PHA) + SUM(Low_Vol_B3_TC) + SUM(LV_Bulk_B3) + SUM(Med_Vol_B3) + SUM(High_Vol_B3)) AS Grand_Total FROM  `t_bpc_number_of_customers_dzongkhag_wise2` a WHERE  a.`Data_Month`=? AND a.`Data_Year`=?) t;");
                        pst.setString(1, repoFormBean.getMonth());
                        pst.setString(2, repoFormBean.getYear());
                    }
                    else {
                        pst = conn.prepareStatement("SELECT t.Data_Year, ROUND(((Total_Low_Vol_Ru/Grand_Total)*100),2) LVRpercent ,        ROUND(((Total_Low_Vol_Ru_Coo/Grand_Total)*100),2)  Ru_Coo_percent,        ROUND(((Total_Low_Vol_Ru_MT/Grand_Total)*100) ,2) Ru_MT_percent,        ROUND(((Total_Low_Vol_Ru_CL/Grand_Total)*100),2)  Ru_CL_percent,        ROUND(((Total_Low_Vol_Urban /Grand_Total)*100),2)  Urban_percent,        ROUND(((Total_Low_Vol_RI /Grand_Total)*100),2)  RI_percent,        ROUND(((Low_Vol_B3_Com/Grand_Total)*100),2) Com_percent,        ROUND(((Low_Vol_B3_Ind/Grand_Total)*100),2) Ind_percent,        ROUND(((Low_Vol_B3_Agr/Grand_Total)*100),2) Agr_percent,        ROUND(((Low_Vol_B3_Ins/Grand_Total)*100),2) Ins_percent,        ROUND(((Low_Vol_B3_SL/Grand_Total)*100),2) SL_percent,        ROUND(((Low_Vol_B3_PHA/Grand_Total)*100),2) PHA_percent,        ROUND(((Low_Vol_B3_TC /Grand_Total)*100),2) TC_percent,        ROUND(((LV_Bulk_B3/Grand_Total)*100),2) LV_Bulk_percent,        ROUND(((Med_Vol_B3/Grand_Total)*100),2) Med_Vol_B3_percent,        ROUND(((High_Vol_B3 /Grand_Total)*100),2) High_Vol_B3_percent,        Total_Low_Vol_Ru,        Total_Low_Vol_Ru_Coo,        Total_Low_Vol_Ru_MT,        Total_Low_Vol_Ru_CL,        Total_Low_Vol_Urban ,        Total_Low_Vol_RI,        Low_Vol_B3_Com ,        Low_Vol_B3_Ind ,        Low_Vol_B3_Agr ,        Low_Vol_B3_Ins ,        Low_Vol_B3_SL ,        Low_Vol_B3_PHA ,        Low_Vol_B3_TC ,        LV_Bulk_B3 ,        Med_Vol_B3 ,        High_Vol_B3 ,        Grand_Total       FROM (SELECT a.Data_Year,(SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) )AS Total_Low_Vol_Ru, \t\t(SUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)) AS Total_Low_Vol_Ru_Coo , \t\t(SUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT))AS Total_Low_Vol_Ru_MT , \t\t(SUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL ))AS Total_Low_Vol_Ru_CL , \t\t(SUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)) AS Total_Low_Vol_Urban , \t\t(SUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) )AS Total_Low_Vol_RI , \t\tSUM(Low_Vol_B3_Com)AS Low_Vol_B3_Com , \t\tSUM(Low_Vol_B3_Ind)AS Low_Vol_B3_Ind , \t\tSUM(Low_Vol_B3_Agr) AS Low_Vol_B3_Agr , \t\tSUM(Low_Vol_B3_Ins)AS Low_Vol_B3_Ins , \t\tSUM(Low_Vol_B3_SL)AS Low_Vol_B3_SL , \t\tSUM(Low_Vol_B3_PHA) AS Low_Vol_B3_PHA , \t\tSUM(Low_Vol_B3_TC)AS Low_Vol_B3_TC , \t\tSUM(LV_Bulk_B3)AS LV_Bulk_B3 , \t\tSUM(Med_Vol_B3)AS Med_Vol_B3 , \t\tSUM(High_Vol_B3) AS High_Vol_B3 , \t    (SUM(Low_Vol_B1_Ru)+SUM(Low_Vol_B2_Ru)+SUM(Low_Vol_B3_Ru) + \t\tSUM(Low_Vol_B1_Ru_Coo)+SUM(Low_Vol_B2_Ru_Coo)+SUM(Low_Vol_B3_Ru_Coo)+ \t\tSUM(Low_Vol_B1_Ru_MT)+SUM(Low_Vol_B2_Ru_MT)+SUM(Low_Vol_B3_Ru_MT)+ \t\tSUM(Low_Vol_B1_Ru_CL) + SUM(Low_Vol_B2_Ru_CL) +SUM( Low_Vol_B3_Ru_CL )+ \t\tSUM(Low_Vol_B1_Urban) + SUM(Low_Vol_B2_Urban) +SUM(Low_Vol_B3_Urban)+ \t\tSUM(Low_Vol_B1_RI)+SUM(Low_Vol_B2_RI)+SUM(Low_Vol_B3_RI) + \t\tSUM(Low_Vol_B3_Com)+ \t\tSUM(Low_Vol_B3_Ind)+ \t\tSUM(Low_Vol_B3_Agr)+ \t\tSUM(Low_Vol_B3_Ins)+ \t\tSUM(Low_Vol_B3_SL)+ \t\tSUM(Low_Vol_B3_PHA)+ \t\tSUM(Low_Vol_B3_TC)+ \t\tSUM(LV_Bulk_B3)+ \t\tSUM(Med_Vol_B3)+ \t\tSUM(High_Vol_B3)) AS Grand_Total \t\tFROM  `t_bpc_number_of_customers_dzongkhag_wise2` \t\ta WHERE a.`Dzongkhag_Id`=? AND a.`Data_Month`=? AND a.`Data_Year`=?) t");
                        pst.setString(1, repoFormBean.getDzongkhagId());
                        pst.setString(2, repoFormBean.getMonth());
                        pst.setString(3, repoFormBean.getYear());
                    }
                    rs = pst.executeQuery();
                    while (rs.next()) {
                        final ReportDTO dto = new ReportDTO();
                        dto.setYear(rs.getString("Data_Year"));
                        dto.setRrpercentage(rs.getString("LVRpercent"));
                        dto.setRcpercentage(rs.getString("Ru_Coo_percent"));
                        dto.setRmtpercentage(rs.getString("Ru_MT_percent"));
                        dto.setRclpercentage(rs.getString("Ru_CL_percent"));
                        dto.setUpercentage(rs.getString("Urban_percent"));
                        dto.setRipercentage(rs.getString("RI_percent"));
                        dto.setCpercentage(rs.getString("Com_percent"));
                        dto.setIpercentage(rs.getString("Ind_percent"));
                        dto.setApercentage(rs.getString("Agr_percent"));
                        dto.setInspercentage(rs.getString("Ins_percent"));
                        dto.setSlpercentage(rs.getString("SL_percent"));
                        dto.setPhapercentage(rs.getString("PHA_percent"));
                        dto.setTcpercentage(rs.getString("TC_percent"));
                        dto.setLvbpercentage(rs.getString("LV_Bulk_percent"));
                        dto.setMvcpercentage(rs.getString("Med_Vol_B3_percent"));
                        dto.setHvcpercentage(rs.getString("High_Vol_B3_percent"));
                        dto.setRrenergysoldmu(rs.getString("Total_Low_Vol_Ru"));
                        dto.setRcenergysoldmu(rs.getString("Total_Low_Vol_Ru_Coo"));
                        dto.setRmtenergysoldmu(rs.getString("Total_Low_Vol_Ru_MT"));
                        dto.setRclenergysoldmu(rs.getString("Total_Low_Vol_Ru_CL"));
                        dto.setUcenergysoldmu(rs.getString("Total_Low_Vol_Urban"));
                        dto.setRicenergysoldmu(rs.getString("Total_Low_Vol_RI"));
                        dto.setCenergysoldmu(rs.getString("Low_Vol_B3_Com"));
                        dto.setIenergysoldmu(rs.getString("Low_Vol_B3_Ind"));
                        dto.setAenergysoldmu(rs.getString("Low_Vol_B3_Agr"));
                        dto.setInsenergysoldmu(rs.getString("Low_Vol_B3_Ins"));
                        dto.setSlenergysoldmu(rs.getString("Low_Vol_B3_SL"));
                        dto.setPhaenergysoldmu(rs.getString("Low_Vol_B3_SL"));
                        dto.setTcenergysoldmu(rs.getString("Low_Vol_B3_TC"));
                        dto.setLvbenergysoldmu(rs.getString("LV_Bulk_B3"));
                        dto.setMvcenergysoldmu(rs.getString("Med_Vol_B3"));
                        dto.setHvcenergysoldmu(rs.getString("High_Vol_B3"));
                        dto.setTotalsoldmu(rs.getString("Grand_Total"));
                        reportList.add(dto);
                    }
                }
                else if (repoFormBean.getReportId().equalsIgnoreCase("9")) {
                    if (repoFormBean.getMonth().equalsIgnoreCase("All")) {
                        pst = conn.prepareStatement("SELECT a.Year, a.`Plant_Name`, \tSUM(a.T1_Energy_Generated) AS T1_Energy_Generated, \tSUM(a.T2_Energy_Generated) AS T2_Energy_Generated, \tSUM(a.Total_Energy_Generated) AS Total_Energy_Generated, \tSUM(a.`T1_Machine_Availability(hrs)`) AS T1_Machine_Availability, \tSUM(a.`T2_Machine_Availability(hrs)`)AS T2_Machine_Availability \tFROM `t_monthly_wind_power` a WHERE a.`Year`=?;");
                        pst.setString(1, repoFormBean.getYear());
                    }
                    else {
                        pst = conn.prepareStatement("SELECT a.Year, a.`Plant_Name`, \tSUM(T1_Energy_Generated) AS T1_Energy_Generated, \tSUM(T2_Energy_Generated) AS T2_Energy_Generated, \tSUM(Total_Energy_Generated) AS Total_Energy_Generated, \tSUM(a.`T1_Machine_Availability(hrs)`) AS T1_Machine_Availability, \tSUM(a.`T2_Machine_Availability(hrs)`)AS T2_Machine_Availability \tFROM `t_monthly_wind_power` a WHERE a.`Month`=? AND  a.`Year`=?;");
                        pst.setString(1, repoFormBean.getMonth());
                        pst.setString(2, repoFormBean.getYear());
                    }
                    rs = pst.executeQuery();
                    while (rs.next()) {
                        final ReportDTO dto = new ReportDTO();
                        dto.setYear(rs.getString("Year"));
                        dto.setPlantname(rs.getString("Plant_Name"));
                        dto.setT1energy(rs.getString("T1_Energy_Generated"));
                        dto.setT2energy(rs.getString("T2_Energy_Generated"));
                        dto.setTotal(rs.getString("Total_Energy_Generated"));
                        dto.setT1available(rs.getString("T1_Machine_Availability"));
                        dto.setT2available(rs.getString("T2_Machine_Availability"));
                        reportList.add(dto);
                    }
                }
                else if (repoFormBean.getReportId().equalsIgnoreCase("10")) {
                    if (repoFormBean.getHydroPlantId().equalsIgnoreCase("All")) {
                        pst = conn.prepareStatement("SELECT a.Year, MONTHNAME(STR_TO_DATE(a.Month, '%M')) MONTHNAME,MONTH(STR_TO_DATE(a.Month, '%M'))numericMonth,  a.Month, SUM(a.Generation)AS Generation, SUM(a.Revenue_From_Export)AS Revenue_From_Export  , SUM(a.Revenue_From_BPC) AS Revenue_From_BPC, SUM(a.Revenue_From_Export+a.Revenue_From_BPC) AS total FROM t_monthly_data_dgpc a WHERE a.Year=? GROUP BY a.Month  ORDER BY MONTH(STR_TO_DATE(a.Month, '%M'));");
                        pst.setString(1, repoFormBean.getYear());
                    }
                    else {
                        pst = conn.prepareStatement("SELECT d.Year, MONTHNAME(STR_TO_DATE(d.Month, '%M')) MONTHNAME,MONTH(STR_TO_DATE(d.Month, '%M'))numericMonth,d.Month, d.Generation, d.Revenue_From_Export, d.Revenue_From_BPC, SUM(d.Revenue_From_Export+d.Revenue_From_BPC) total FROM t_monthly_data_dgpc d WHERE d.Plant_Id=? AND d.Year=? GROUP BY d.Month  ORDER BY MONTH(STR_TO_DATE(d.Month, '%M'))");
                        pst.setString(1, repoFormBean.getHydroPlantId());
                        pst.setString(2, repoFormBean.getYear());
                    }
                    rs = pst.executeQuery();
                    while (rs.next()) {
                        final ReportDTO dto = new ReportDTO();
                        dto.setYear(rs.getString("Year"));
                        dto.setMonth(rs.getString("monthName"));
                        dto.setNumericMonth(rs.getString("numericMonth"));
                        dto.setGeneration(rs.getString("Generation"));
                        dto.setExport(rs.getString("Revenue_From_Export"));
                        dto.setInternal(rs.getString("Revenue_From_BPC"));
                        dto.setTotal(rs.getString("total"));
                        reportList.add(dto);
                    }
                }
                else if (repoFormBean.getReportId().equalsIgnoreCase("11")) {
                    if (repoFormBean.getMonth().equalsIgnoreCase("All")) {
                        pst = conn.prepareStatement("SELECT  a.`Plant_Name`, \ta.`Energy_Purchase_MU`, \ta.`Energy_Purchase_Payment`, \ta.`Energy_wheeled_MU`, \ta.`Energy_wheeled_Revenue`, \ta.`Energy_Sale_Mu`, \ta.`Energy_Sale_Revenue` FROM `t_bpc_energy_purchase2`a WHERE a.`Data_Year`=?;");
                        pst.setString(1, repoFormBean.getYear());
                    }
                    else {
                        pst = conn.prepareStatement("SELECT  a.`Plant_Name`, \ta.`Energy_Purchase_MU`, \ta.`Energy_Purchase_Payment`, \ta.`Energy_wheeled_MU`, \ta.`Energy_wheeled_Revenue`, \ta.`Energy_Sale_Mu`, \ta.`Energy_Sale_Revenue` FROM `t_bpc_energy_purchase2`a WHERE a.`Data_Month`=? AND a.`Data_Year`=?;");
                        pst.setString(1, repoFormBean.getMonth());
                        pst.setString(2, repoFormBean.getYear());
                    }
                    rs = pst.executeQuery();
                    while (rs.next()) {
                        final ReportDTO dto = new ReportDTO();
                        dto.setPlantName(rs.getString("Plant_Name"));
                        dto.setEnergyPurchaseMU(rs.getString("Energy_Purchase_MU"));
                        dto.setEnergyPurchasePayment(rs.getString("Energy_Purchase_Payment"));
                        dto.setEnergyWheeledMU(rs.getString("Energy_wheeled_MU"));
                        dto.setEnergyWheeledRevenue(rs.getString("Energy_wheeled_Revenue"));
                        dto.setEnergySaleMU(rs.getString("Energy_Sale_Mu"));
                        dto.setEnergySaleRevenue(rs.getString("Energy_Sale_Revenue"));
                        reportList.add(dto);
                    }
                }
                else if (repoFormBean.getReportId().equalsIgnoreCase("12")) {
                    if (repoFormBean.getHydroPlantId().equalsIgnoreCase("All") && repoFormBean.getMonth().equalsIgnoreCase("All")) {
                        pst = conn.prepareStatement("SELECT a.Plant_Name, a.Year, MONTHNAME(STR_TO_DATE(a.Month, '%M')) MONTHNAME,MONTH(STR_TO_DATE(a.Month, '%M'))numericMonth,  a.Month, a.Generation, a.Export_MU, a.Sale_To_BPC_MU, a.Export_Tariff, a.Domestic_Tariff, a.Revenue_From_Export, a.Revenue_From_BPC FROM t_monthly_data_dgpc a WHERE a.Year = ?  GROUP BY a.Plant_Id,MONTH(STR_TO_DATE(a.Month, '%M')) ORDER BY a.Plant_Id,MONTH(STR_TO_DATE(a.Month, '%M'))");
                        pst.setString(1, repoFormBean.getYear());
                    }
                    else if (repoFormBean.getHydroPlantId().equalsIgnoreCase("All")) {
                        pst = conn.prepareStatement("SELECT a.Plant_Name, a.Year, MONTHNAME(STR_TO_DATE(a.Month, '%M')) MONTHNAME,MONTH(STR_TO_DATE(a.Month, '%M'))numericMonth,a.Month, a.Generation, a.Generation, a.Export_MU, a.Sale_To_BPC_MU, a.Export_Tariff, a.Domestic_Tariff, a.Revenue_From_Export, a.Revenue_From_BPC FROM t_monthly_data_dgpc a WHERE a.Month =? AND  a.Year = ? GROUP BY a.Plant_Id");
                        pst.setString(1, repoFormBean.getMonth());
                        pst.setString(2, repoFormBean.getYear());
                    }
                    else if (repoFormBean.getMonth().equalsIgnoreCase("All")) {
                        pst = conn.prepareStatement("SELECT a.Plant_Name, a.Year, MONTHNAME(STR_TO_DATE(a.Month, '%M')) MONTHNAME,MONTH(STR_TO_DATE(a.Month, '%M'))numericMonth,a.Month, a.Generation, a.Export_MU, a.Sale_To_BPC_MU, a.Export_Tariff, a.Domestic_Tariff, a.Revenue_From_Export, a.Revenue_From_BPC FROM t_monthly_data_dgpc a WHERE a.Plant_Id=? AND  a.Year = ? ORDER BY MONTH(STR_TO_DATE(a.Month, '%M'))");
                        pst.setString(1, repoFormBean.getHydroPlantId());
                        pst.setString(2, repoFormBean.getYear());
                    }
                    else {
                        pst = conn.prepareStatement("SELECT a.Plant_Name, a.Year, MONTHNAME(STR_TO_DATE(a.Month, '%M')) MONTHNAME,MONTH(STR_TO_DATE(a.Month, '%M'))numericMonth,a.Month, a.Generation, a.Export_MU,a .Sale_To_BPC_MU, a.Export_Tariff, a.Domestic_Tariff, a.Revenue_From_Export, a.Revenue_From_BPC FROM t_monthly_data_dgpc a WHERE a.Plant_Id=? AND a.Month =? AND a.Year = ?");
                        pst.setString(1, repoFormBean.getHydroPlantId());
                        pst.setString(2, repoFormBean.getMonth());
                        pst.setString(3, repoFormBean.getYear());
                    }
                    rs = pst.executeQuery();
                    while (rs.next()) {
                        final ReportDTO dto = new ReportDTO();
                        dto.setPlantName(rs.getString("Plant_Name"));
                        dto.setYear(rs.getString("Year"));
                        dto.setMonth(rs.getString("MONTHNAME"));
                        dto.setGeneration(rs.getString("Generation"));
                        dto.setExportMU(rs.getString("Export_MU"));
                        dto.setSaleToBPCMU(rs.getString("Sale_To_BPC_MU"));
                        dto.setExportTariff(rs.getString("Export_Tariff"));
                        dto.setGenerationTariff(rs.getString("Domestic_Tariff"));
                        dto.setRevenueFromExport(rs.getString("Revenue_From_Export"));
                        dto.setRevenueFromBPC(rs.getString("Revenue_From_BPC"));
                        reportList.add(dto);
                    }
                }
            }
        }
        catch (Exception e) {
            e.printStackTrace();
            throw new HPSException("###Error at AdminDAO[getGeneratReportList]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return reportList;
    }
    
    public static List<AdminDTO> getHydropowerInstalledCapacityListMW() throws HPSException, HPSSystemException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        final List<AdminDTO> installedCapacityList = new ArrayList<AdminDTO>();
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(AdminDAO.GET_HYDROPOWER_INSATLLED_CAPACITY);
                rs = pst.executeQuery();
                while (rs.next()) {
                    final AdminDTO dto = new AdminDTO();
                    dto.setPlantname(rs.getString("Plant_Name"));
                    dto.setInstalCapicityMW(rs.getString("Installed_Capacity"));
                    dto.setOperationDate(rs.getString("COD"));
                    installedCapacityList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException();
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return installedCapacityList;
    }
    
    public static List<AdminDTO> getMinihydroInstalledCapacityListMW() throws HPSException, HPSSystemException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        final List<AdminDTO> installedCapacityList = new ArrayList<AdminDTO>();
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(AdminDAO.GET_MINIHYDRO_INSATLLED_CAPACITY);
                rs = pst.executeQuery();
                while (rs.next()) {
                    final AdminDTO dto = new AdminDTO();
                    dto.setPlantname(rs.getString("Plant_Name"));
                    dto.setInstalCapicityMW(rs.getString("Installed_Capacity"));
                    installedCapacityList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException();
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return installedCapacityList;
    }
    
    public static List<AdminDTO> getWindpowerInstalledCapacityListMW() throws HPSException, HPSSystemException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        final List<AdminDTO> installedCapacityList = new ArrayList<AdminDTO>();
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(AdminDAO.GET_WINDPOWER_INSATLLED_CAPACITY);
                rs = pst.executeQuery();
                while (rs.next()) {
                    final AdminDTO dto = new AdminDTO();
                    dto.setPlantname(rs.getString("Plant_Name"));
                    dto.setInstalCapicityMW(rs.getString("Installed_Capacity"));
                    installedCapacityList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException();
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return installedCapacityList;
    }
    
    public static List<AdminDTO> getSolarpowerInstalledCapacityListMW() throws HPSException, HPSSystemException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        final List<AdminDTO> installedCapacityList = new ArrayList<AdminDTO>();
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(AdminDAO.GET_SOLARPOWER_INSATLLED_CAPACITY);
                rs = pst.executeQuery();
                while (rs.next()) {
                    final AdminDTO dto = new AdminDTO();
                    dto.setPlantname(rs.getString("Plant_Name"));
                    dto.setInstalCapicityMW(rs.getString("Installed_Capacity"));
                    installedCapacityList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException();
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return installedCapacityList;
    }
    
    public static List<AdminDTO> getDgInstalledCapacityListMW() throws HPSException, HPSSystemException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        final List<AdminDTO> installedCapacityList = new ArrayList<AdminDTO>();
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(AdminDAO.GET_DG_PLANT_INSATLLED_CAPACITY);
                rs = pst.executeQuery();
                while (rs.next()) {
                    final AdminDTO dto = new AdminDTO();
                    dto.setPlantname(rs.getString("Plant_Name"));
                    dto.setInstalCapicityMW(rs.getString("Installed_Capacity"));
                    installedCapacityList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException();
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return installedCapacityList;
    }
    
    public static List<AdminDTO> getPlantWiseTotalGenerationListMU(final String dateTotalGenMUPlantWise) throws HPSException, HPSSystemException, ParseException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        final List<AdminDTO> installedCapacityList = new ArrayList<AdminDTO>();
        final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
        final java.util.Date date = sdfsource.parse(dateTotalGenMUPlantWise);
        final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
        final String Newdate = sdf.format(date);
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(AdminDAO.GET_TOTAL_GENERATION_MU_PLANT_WISE);
                pst.setString(1, Newdate);
                rs = pst.executeQuery();
                while (rs.next()) {
                    final AdminDTO dto = new AdminDTO();
                    dto.setPlantname(rs.getString("Plant_Name"));
                    dto.setTotalGenMU(rs.getString("Total_MU"));
                    installedCapacityList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException();
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return installedCapacityList;
    }
    
    public static List<AdminDTO> getSubstationWiseTotalDemandListMW(final String dateToalDemandMWSubstationWise) throws HPSException, HPSSystemException, ParseException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        final List<AdminDTO> totalDemandSubstationWiseListMW = new ArrayList<AdminDTO>();
        final SimpleDateFormat sdfsource = new SimpleDateFormat("dd/mm/yyyy");
        final java.util.Date date = sdfsource.parse(dateToalDemandMWSubstationWise);
        final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-mm-dd");
        final String Newdate = sdf.format(date);
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(AdminDAO.GET_TOTAL_DEMAND_SUB_STATION_WISE);
                pst.setString(1, Newdate);
                rs = pst.executeQuery();
                while (rs.next()) {
                    final AdminDTO dto = new AdminDTO();
                    dto.setSubStationName(rs.getString("Sub_Station_Name"));
                    dto.setTaoalDemandMW(rs.getString("Higest_MW"));
                    totalDemandSubstationWiseListMW.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException();
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return totalDemandSubstationWiseListMW;
    }
    
    public String updateUserPassword(final String uid, final String password) {
        PreparedStatement pst = null;
        String result = "UPDATE_FAILURE";
        final ResultSet rs = null;
        Connection connection = null;
        try {
            final String salt = PasswordEncryptionUtil.generateSalt(512).get();
            final String hashPassword = PasswordEncryptionUtil.hashPassword(password, salt).get();
            connection = ConnectionManager.getConnection();
            pst = connection.prepareStatement("UPDATE t_user_master a SET a.`Password_Salt`=?,a.`Password`=? WHERE a.`User_Id` = ?");
            pst.setString(1, salt);
            pst.setString(2, hashPassword);
            pst.setString(3, uid);
            pst.executeUpdate();
            result = "UPDATE_SUCCESS";
        }
        catch (Exception e) {
            e.printStackTrace();
            result = "UPDATE_FAILURE";
            return result;
        }
        finally {
            ConnectionManager.close(connection, rs, pst);
        }
        ConnectionManager.close(connection, rs, pst);
        return result;
    }
    
    public String startDatabaseBackup() throws HPSException, HPSSystemException {
        final AdminDTO dto = new AdminDTO();
        String result = "DATABASE_BACKUP_FAILURE";
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement("SELECT `Mysql_Path`,`Database_Name`,`Database_User_Name`,`Database_Password`,`Database_Host`,`Backup_Path` FROM `t_database_config_master`");
                rs = pst.executeQuery();
                if (rs.next()) {
                    dto.setMysqlPath(rs.getString("Mysql_Path"));
                    dto.setDatabaseName(rs.getString("Database_Name"));
                    dto.setDatabaseUsername(rs.getString("Database_User_Name"));
                    dto.setDatabasePassword(rs.getString("Database_Password"));
                    dto.setDatabaseHost(rs.getString("Database_Host"));
                    dto.setDatabaseBackupPath(rs.getString("Backup_Path"));
                }
                final boolean isDBCreated = DatabaseUtil.dbBackup(dto);
                if (isDBCreated) {
                    result = "DATABASE_BACKUP_SUCCESS";
                }
            }
        }
        catch (Exception e) {
            result = "DATABASE_BACKUP_FAILURE";
            throw new HPSException("###Error at AdminDAO[startDatabaseBackup]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return result;
    }
    
    public String editDatabaseConfigDtls(final AdminDTO dto) throws HPSException, HPSSystemException {
        String result = "DATABASE_EDIT_FAILURE";
        Connection conn = null;
        PreparedStatement pst = null;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" UPDATE  `t_database_config_master`  SET  `Mysql_Path` = ?,  `Database_Name` = ?,  `Database_User_Name` = ?,  `Database_Password` = ?,  `Database_Host` = ?,  `Backup_Path` = ?");
                pst.setString(1, dto.getMysqlPath());
                pst.setString(2, dto.getDatabaseName());
                pst.setString(3, dto.getDatabaseUsername());
                pst.setString(4, dto.getDatabasePassword());
                pst.setString(5, dto.getDatabaseHost());
                pst.setString(6, dto.getDatabaseBackupPath());
                final int count = pst.executeUpdate();
                if (count > 0) {
                    result = "DATABASE_EDIT_SUCCESS";
                }
            }
        }
        catch (Exception e) {
            result = "DATABASE_EDIT_FAILURE";
            throw new HPSException("###Error at AdminDAO[editDatabaseConfigDtls]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, (ResultSet)null, pst);
        }
        ConnectionManager.close(conn, (ResultSet)null, pst);
        return result;
    }
    
    public List<DatabaseConfigDTO> getDatabaseConfigDtls() throws HPSException, HPSSystemException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet rs = null;
        final List<DatabaseConfigDTO> dbConfigList = new ArrayList<DatabaseConfigDTO>();
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement("SELECT `Mysql_Path`,`Database_Name`,`Database_User_Name`,`Database_Password`,`Database_Host`,`Backup_Path` FROM `t_database_config_master`");
                rs = pst.executeQuery();
                while (rs.next()) {
                    final DatabaseConfigDTO dto = new DatabaseConfigDTO();
                    dto.setMysqlPath(rs.getString("Mysql_Path"));
                    dto.setDatabaseName(rs.getString("Database_Name"));
                    dto.setDatabaseUserName(rs.getString("Database_User_Name"));
                    dto.setDatabasePassword(rs.getString("Database_Password"));
                    dto.setDatabaseHost(rs.getString("Database_Host"));
                    dto.setDatabaseBackupPath(rs.getString("Backup_Path"));
                    dbConfigList.add(dto);
                }
            }
        }
        catch (Exception e) {
            throw new HPSException("###Error at AdminDAO[getDatabaseConfigDtls]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return dbConfigList;
    }
    
    public String notifyManagement(final String notifyId) throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        final ResultSet rs = null;
        String result = "FAILURE";
        String query = null;
        try {
            query = "UPDATE `t_user_notification_mapping` a SET a.`Is_Deleted` = 'Y' WHERE a.`User_notify_id` = ?";
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            if (conn != null) {
                pst = conn.prepareStatement(query);
                pst.setString(1, notifyId);
                final int count = pst.executeUpdate();
                if (count > 0) {
                    result = "SUCCESS";
                    conn.commit();
                }
            }
        }
        catch (Exception e) {
            conn.rollback();
            result = "FAILURE";
            throw new HPSException("###Error at AdminDAO[notifyManagement]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return result;
    }
    
    public String composeManagement(final String notifyId) throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        final ResultSet rs = null;
        String result = "FAILURE";
        String query = null;
        try {
            query = "UPDATE `t_notification_details` a SET a.`Is_Deleted` = 'Y' WHERE a.`Notification_Id` = ?";
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            if (conn != null) {
                pst = conn.prepareStatement(query);
                pst.setString(1, notifyId);
                final int count = pst.executeUpdate();
                if (count > 0) {
                    result = "SUCCESS";
                    conn.commit();
                }
            }
        }
        catch (Exception e) {
            conn.rollback();
            result = "FAILURE";
            throw new HPSException("###Error at AdminDAO[composeManagement]:exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, rs, pst);
        }
        ConnectionManager.close(conn, rs, pst);
        return result;
    }
    
    public String addNotifications(final AdminDTO dto, final UserRolePriviledge userRolePriv) throws HPSException, HPSSystemException, SQLException {
        Connection conn = null;
        PreparedStatement pst = null;
        ResultSet resultSet = null;
        String result = null;
        String notifyId = null;
        try {
            conn = ConnectionManager.getConnection();
            conn.setAutoCommit(false);
            if (conn != null) {
                pst = conn.prepareStatement("INSERT INTO `t_notification_details`(`Notification_Title`,`Notification`,`Created_By`,`Created_Date`) VALUES (?,?,?,CURRENT_TIMESTAMP);");
                pst.setString(1, dto.getNotifyTitle());
                pst.setString(2, dto.getNotifyText());
                pst.setString(3, userRolePriv.getUserId());
                final int count = pst.executeUpdate();
                if (count > 0) {
                    pst = conn.prepareStatement("SELECT a.`Notification_Id` FROM `t_notification_details` a ORDER BY  a.`Notification_Id` DESC LIMIT 1");
                    resultSet = pst.executeQuery();
                    while (resultSet.next()) {
                        notifyId = resultSet.getString("Notification_Id");
                    }
                    final String notifyID = notifyId;
                    if (dto.getRoleId().equalsIgnoreCase("4")) {
                        pst = conn.prepareStatement("SELECT a.`User_Id` FROM `t_user_master` a LEFT JOIN `t_user_role_mapping` b ON a.`User_Id` = b.`User_Id` WHERE b.`Role_Id` ='4' AND a.`Is_Active` ='Y'");
                    }
                    if (dto.getRoleId().equalsIgnoreCase("3")) {
                        if (dto.getSubstationId().equalsIgnoreCase("All")) {
                            pst = conn.prepareStatement("SELECT a.`User_Id` FROM `t_user_master` a LEFT JOIN `t_user_role_mapping` b ON a.`User_Id` = b.`User_Id` WHERE b.`Role_Id` ='3' AND a.`Is_Active` ='Y'");
                        }
                        else {
                            pst = conn.prepareStatement("SELECT a.`User_Id` FROM `t_user_master` a LEFT JOIN `t_user_role_mapping` b ON a.`User_Id` = b.`User_Id` LEFT JOIN `t_sub_station_master` c ON a.`Location_Id` = c.`Substation_Code` WHERE b.`Role_Id` ='3' AND c.`Substation_Code` = ? AND a.`Is_Active` ='Y';");
                            pst.setString(1, dto.getSubstationId());
                        }
                    }
                    if (dto.getRoleId().equalsIgnoreCase("All")) {
                        pst = conn.prepareStatement("SELECT b.`User_Id` FROM `t_user_role_mapping` b WHERE b.`Role_Id` IN ('3','4') AND b.`User_Id` IN (SELECT User_Id FROM `t_user_master` WHERE `Is_Active`= 'Y')");
                    }
                    resultSet = pst.executeQuery();
                    while (resultSet.next()) {
                        this.getInsertIntoMappingTbl(notifyID, resultSet.getString("User_Id"), conn);
                    }
                    result = "ADD_USER_SUCCESS";
                    conn.commit();
                }
            }
        }
        catch (Exception e) {
            e.printStackTrace();
            conn.rollback();
            result = "ADD_USER_FAILURE";
            throw new HPSException("###Error at AdminDAO[addNotifications]: exception:: " + e);
        }
        finally {
            ConnectionManager.close(conn, (ResultSet)null, pst);
        }
        ConnectionManager.close(conn, (ResultSet)null, pst);
        return result;
    }
    
    private String getInsertIntoMappingTbl(final String notifyID, final String uId, final Connection conn) throws HPSException, HPSSystemException {
        PreparedStatement pst = null;
        final ResultSet rs = null;
        final String count = "0";
        String query = null;
        try {
            if (conn != null) {
                query = "INSERT INTO `t_user_notification_mapping` (`Notification_Id`,`User_Id`) VALUES (?,?);";
                pst = conn.prepareStatement(query);
                pst.setString(1, notifyID);
                pst.setString(2, uId);
                pst.executeUpdate();
            }
        }
        catch (Exception e) {
            throw new HPSException("###Error at CommonDAO[getInsertIntoMappingTbl]:exception:: " + e);
        }
        finally {
            ConnectionManager.close((Connection)null, rs, pst);
        }
        ConnectionManager.close((Connection)null, rs, pst);
        return count;
    }
    
    public String editEmailConfigDtls(final AdminDTO dto) throws HPSException, HPSSystemException {
        Connection conn = null;
        PreparedStatement pst = null;
        String result = "EMAIL_EDIT_FAILURE";
        int count = 0;
        try {
            conn = ConnectionManager.getConnection();
            if (conn != null) {
                pst = conn.prepareStatement(" UPDATE  `t_email_config_master`  SET  `Configuration` = ?  WHERE Config_Type = ?");
                pst.setString(1, dto.getSmtpHost());
                pst.setString(2, "HOST_ADDRESS");
                count = pst.executeUpdate();
                pst = conn.prepareStatement(" UPDATE  `t_email_config_master`  SET  `Configuration` = ?  WHERE Config_Type = ?");
                pst.setString(1, dto.getSmtpPort());
                pst.setString(2, "SMTP_PORT");
                count = pst.executeUpdate();
                pst = conn.prepareStatement(" UPDATE  `t_email_config_master`  SET  `Configuration` = ?  WHERE Config_Type = ?");
                pst.setString(1, dto.getMailDebugFlag());
                pst.setString(2, "DEBUG_FLAG");
                count = pst.executeUpdate();
                pst = conn.prepareStatement(" UPDATE  `t_email_config_master`  SET  `Configuration` = ?  WHERE Config_Type = ?");
                pst.setString(1, dto.getMailStartTlsFlag());
                pst.setString(2, "STARTTLS_ENABLE_FLAG");
                count = pst.executeUpdate();
                pst = conn.prepareStatement(" UPDATE  `t_email_config_master`  SET  `Configuration` = ?  WHERE Config_Type = ?");
                pst.setString(1, dto.getFromAddress());
                pst.setString(2, "FROM_ADDRESS");
                count = pst.executeUpdate();
                pst = conn.prepareStatement(" UPDATE  `t_email_config_master`  SET  `Configuration` = ?  WHERE Config_Type = ?");
                pst.setString(1, dto.getMailUserId());
                pst.setString(2, "MAIL_USER_ADDRESS");
                count = pst.executeUpdate();
                pst = conn.prepareStatement(" UPDATE  `t_email_config_master`  SET  `Configuration` = ?  WHERE Config_Type = ?");
                pst.setString(1, dto.getMailUserPassword());
                pst.setString(2, "MAIL_USER_PASSWORD");
                count = pst.executeUpdate();
                pst = conn.prepareStatement(" UPDATE  `t_email_config_master`  SET  `Configuration` = ?  WHERE Config_Type = ?");
                pst.setString(1, dto.getSmtpAuthFlag());
                pst.setString(2, "SMTP_AUTH_FLAG");
                count = pst.executeUpdate();
                if (count > 0) {
                    result = "EMAIL_EDIT_SUCCESS";
                }
            }
        }
        catch (Exception e) {
            result = "EMAIL_EDIT_FAILURE";
            throw new HPSException("###Error at AdminDAO[editEmailConfigDtls]:exception: " + e);
        }
        ConnectionManager.close(conn, (ResultSet)null, pst);
        return result;
    }
}
