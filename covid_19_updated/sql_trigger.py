
###-----++++++++++++++++++++++++++++++++++ DEATCH_201902_18516_PP_PPWC_Paid_Off_Rejecters_Still_Approved.+++++++++++++++-----

Suppression_paid_off_rejector_approved='''

                drop table pp_oap_mrkishore_t_t.gm_de_18516_Rejecters_Still_Approved;
                create table pp_oap_mrkishore_t_t.gm_de_18516_Rejecters_Still_Approved as
                (
                select   a.cust_id, 
                case when c.pp_cust_id is not null then 'P'else 'G'end as segment,c.pre_approved_offer30pc,
                case when segment = 'P' then  c.pre_approved_end_date  else null end as pre_approved_expiry_date,
                case when segment = 'P' then (trim(extract( day from pre_Approved_end_date))||'/'||trim(extract (Month from pre_Approved_end_date))||'/'||trim(extract(Year from pre_Approved_end_date))) else null  end as expiry_date,
                case when segment = 'P' then  c.pre_approved_offer30pc  else null end as loan_amt, 
                substr(trim(trailing'.' from '£'||trim(cast(c.pre_approved_offer30pc  as decimal (10,0)))) ,1,length(trim(trailing'.' from '£'||trim(cast(c.pre_approved_offer30pc  as decimal (10,0)))) )/2)||','||substr(trim(trailing'.' from '£'||trim(cast(c.pre_approved_offer30pc  as decimal (10,0)))) ,(length(trim(trailing'.' from '£'||trim(cast(c.pre_approved_offer30pc  as decimal (10,0)))) )/2)+1,3) as loan_amount_final,
                case when a.busn_name='#' then cust_first_name else a.busn_name end as Business_Name 
                from     pp_odm_views.dim_cust_prfl a join    pp_discovery_views.dim_customer b on    a.cust_id = b.cust_id    and    prmry_reside_cntry_code = 'DE'    and    a.PPWC_ACTV_FLAG=1    and    a.PPWC_MKT_SUPP_Y_N = 'N'  left join pp_risk_roe_views.PA_for_Pluto_n_Mktg c on a.cust_id = c.pp_cust_id and c.pre_approved_end_date>=current_date
                ) with data primary index (cust_id);


                CREATE TABLE PP_OAP_MRKISHORE_T_T.UM_suppressed_list_temp as (
				SELECT count(a.cust_id)
                        from PP_ODM_VIEWS.dim_cust_prfl a 
                        join pp_odm_views.dim_mkt_glbl_cust c  
                        on a.cust_id=c.latin_cust_id    
                        join PP_ODM_VIEWS.DIM_MKT_EU_CUST e
                        on a.cust_id=e.latin_cust_id
                        join pp_oap_mrkishore_t_t.gm_de_18516_Rejecters_Still_Approved f
                        on cast(a.CUST_ID as decimal(20,0)) =cast(f.CUST_ID as decimal(20,0))
--                        
                       
                        WHERE
                        c.glbl_suppression_y_n='N'
                        and c.prmry_reside_cntry_code='DE'
                        and c.prmry_email_vrfd_dt > '1969-12-31'
                        and c.emailable_status_y_n='Y'
                        and c.mth_newsletter_y_n='Y'
                       
                        and c.cust_cre_dt>=current_date-90
                        and c.cust_acct_type_code IN (1,2)
--                       
                                                
                        
                       
--                         ---------EXCLUSION---------

                        --- Last minute Suppression
                        and c.cust_id not in (select cust_id from PP_OAP_MRKISHORE_T_T.Last_minute_Exclusions_COPY)
                        and a.cust_id not in (sel customer_id from PP_OAP_MRKISHORE_T_T.uk_ppwc_trigger_banner_exclusion_1_COPY)
                        and a.cust_id not in (sel customer_id from PP_OAP_MRKISHORE_T_T.uk_ppwc_trigger_banner_exclusion_2_COPY)

                        
						----  eTsy_B2B:
                        and  not (e.prmry_email_addr like '%payments_noreply+%')
 							
						
						--- Null Encrypted Email ID:
--                        and not (e.encrypt_email_addr = '#' OR e.encrypt_email_addr = '')
                      
                         ---FA Exclusion
                        and a.cust_id not in (sel Merchant_id from PP_OAP_MRKISHORE_T_T.SNPT_UG_FA_APP_MERCH_COPY)
                        
	                      ------Open Advances:
							and cast(a.CUST_ID as decimal(20,0)) NOT IN(
							select a.cust_id 
							from PP_ODM_VIEWS.DIM_MKT_EU_CUST a
							join  PP_CR_MERCH_DI_ACCESS_VIEWS.dim_cr_merch_acct b
							on cast(b.current_pp_cust_id as decimal(20,0))= cast(a.latin_cust_id as decimal(20,0))
							where b.loan_close_dt ='2099/01/01'
							group by 1
							)
                            
                      )with data unique primary index(cust_id);

--                       '''



#### Segmentation Logic ######

##-1. D0:
segmntation_D0_special_table='''
                drop table PP_OAP_MRKISHORE_T_T.md_DE_18516_rejecters;
                create table PP_OAP_MRKISHORE_T_T.md_DE_18516_rejecters as
                (
                select  m.cust_id,    
                'yes' as rejecters, segment,    loan_amt 
                from  pp_unica.gm_de_18516_Rejecters_Still_Approved m join    
                (select pp_cust_id, dcsn_status, cr_merch_appl_dt,cr_merch_appl_ts    
                from pp_cr_merch_di_access_views.fact_cr_merch_appl    qualify row_number() 
                over (partition by pp_cust_id order by (cr_merch_appl_ts) desc ) = 1    ) last_app 
                on m.cust_id = last_app.pp_cust_id left join    
                (select current_pp_cust_id, loan_cre_dt, loan_paid_off_y_n, loan_close_dt    
                from pp_cr_merch_di_access_views.dim_cr_merch_acct     
                QUALIFY ROW_NUMBER() OVER (PARTITION BY current_pp_cust_id ORDER BY (loan_cre_dt) DESC) = 1     
                ) 
                last_loan on m.cust_id = last_loan.current_pp_cust_id 
                where   last_app.dcsn_status like '%pprov%' 
                and    ((loan_cre_dt is null) or (cr_merch_appl_dt >= loan_close_dt))    
                and    cr_merch_appl_dt <= current_date - 2  
                and (current_date - cr_merch_appl_dt) >15
                ) with data primary index (cust_id);

'''

segment_D0 ='''
sel a.cust_id from PP_OAP_MRKISHORE_T_T.UM_suppressed_list_temp a
join pp_oap_mrkishore_t_t.md_DE_18516_rejecters b
on a.cust_id = b.cust_id
join pp_oap_mrkishore_t_t.gm_de_18516_Rejecters_Still_Approved c
on a.cust_id=c.cust_id

where 
cast(a.cust_id as decimal(20,0)) not in (
sel cast(cust_id as decimal(20,0)) from PP_UNICA_ACCESS_VIEWS.DW_UA_CUST_CONTACT_HISTORY
where CMPGN_CODE = '000016931
)
and EXTRACT (DAY FROM CURRENT_DATE) >14
and pp_oap_mrkishore_t_t.gm_de_18516_Rejecters_Still_Approved.segment='G'


'''

# --2. D14:
# ------------
segmentation_D14='''

                sel cust_id from PP_OAP_MRKISHORE_T_T.UM_suppressed_list_temp 

                where

                CUST_ID IN
                (

                SELECT H.CUST_ID FROM
                PP_UNICA_ACCESS_VIEWS.DW_UA_CUST_CONTACT_HISTORY H 
                JOIN PP_ACCESS_VIEWS.DW_UA_TREATMENT t  
                ON t.treatment_pkg_id=h.cntct_pack_id 
                and t.treatment_cell_id=h.cntct_hist_cellid
                join PP_ACCESS_VIEWS.DW_UA_OFFER O 
                ON T.treatment_ofr_id=O.ofr_id


                WHERE a.CMPGN_CODE = '000016931'
                AND
                a.CNTCT_HIST_DATE >= CURRENT_DATE() - 25
                AND
                ----MKDW_PP_UNICA_CONTACT_HISTORY_Dim.PPAV_DW_UA_TREATMENT.PPAV_DW_UA_OFFER.ofr_id = 000837297
                O.ofr_id = 000837297

                )

                AND CUST_ID NOT IN
                (
                select a.cust_id 
                from PP_ODM_VIEWS.DIM_MKT_EU_CUST a
                join  PP_CR_MERCH_DI_ACCESS_VIEWS.FACT_CR_merch_appl b
                on b.pp_cust_id= a.latin_cust_id
                JOIN PP_UNICA_ACCESS_VIEWS.DW_UA_CUST_CONTACT_HISTORY H
                ON A.LATIN_CUST_ID=H.CUST_ID
                WHERE CMPGN_CODE = '000016931'
                AND b.cr_merch_appl_dt >= CURRENT_DATE () - 25
                group by 1;
                )

        '''

# --3. D29 :
# --------------
segment_D29 ='''

sel cust_id from PP_OAP_MRKISHORE_T_T.UM_suppressed_list_temp 

where

CUST_ID IN
(

SELECT H.CUST_ID FROM
PP_UNICA_ACCESS_VIEWS.DW_UA_CUST_CONTACT_HISTORY H 
JOIN PP_ACCESS_VIEWS.DW_UA_TREATMENT t  
ON t.treatment_pkg_id=h.cntct_pack_id 
and t.treatment_cell_id=h.cntct_hist_cellid
join PP_ACCESS_VIEWS.DW_UA_OFFER O 
ON T.treatment_ofr_id=O.ofr_id

where H.CMPGN_CODE = '000016931'
AND
(H.CNTCT_HIST_DATE between (CURRENT_DATE() - 40) and (CURRENT_DATE() - 26) )
AND
O.ofr_id in
(
837297
)
)
AND 
CUST_ID IN
(
SELECT H.CUST_ID FROM
PP_UNICA_ACCESS_VIEWS.DW_UA_CUST_CONTACT_HISTORY H 
JOIN PP_ACCESS_VIEWS.DW_UA_TREATMENT t  
ON t.treatment_pkg_id=h.cntct_pack_id 
and t.treatment_cell_id=h.cntct_hist_cellid
join PP_ACCESS_VIEWS.DW_UA_OFFER O 
ON T.treatment_ofr_id=O.ofr_id


WHERE H.CMPGN_CODE = '000016931'
AND
H.CNTCT_HIST_DATE >= CURRENT_DATE() - 25
AND
O.ofr_id in
(
837301
)
)
AND CUST_ID NOT IN
(
select a.cust_id 
from PP_ODM_VIEWS.DIM_MKT_EU_CUST a
join  PP_CR_MERCH_DI_ACCESS_VIEWS.FACT_CR_merch_appl b
on b.pp_cust_id= a.latin_cust_id
JOIN PP_UNICA_ACCESS_VIEWS.DW_UA_CUST_CONTACT_HISTORY H
ON A.LATIN_CUST_ID=H.CUST_ID
WHERE CMPGN_CODE = '000016931'
AND b.cr_merch_appl_dt >= CURRENT_DATE () - 25
group by 1;
)
'''