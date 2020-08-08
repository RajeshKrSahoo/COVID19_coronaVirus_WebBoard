# import io
# import random
# from flask import Response,Flask
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.figure import Figure
# app = Flask(__name__)

# @app.route('/plot')
# def plot_png():
#     fig = create_figure()
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')

# def create_figure():
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1)
#     xs = range(100)
#     ys = [random.randint(1, 50) for x in xs]
#     axis.plot(xs, ys)
#     return fig


# if __name__ == '__main__':
    
#     # app.run(debug=True)
#     from werkzeug.serving import run_simple
#     run_simple('localhost', 9004, app)



CREATE MULTISET TABLE PP_OAP_HARSAGARWAL_T.SNPT_UG_F6781_PRE_AUD_MP
AS
(
SELECT LATIN_CUST_ID FROM pp_odm_views.dim_mkt_glbl_cust
WHERE
prmry_reside_cntry_code = 'GB'
AND
emailable_status_y_n = 'Y'
AND
mth_newsletter_y_n = 'Y'
AND
cust_acct_type_code in (2)
AND
glbl_suppression_y_n = 'N' 
) WITH DATA PRIMARY INDEX(LATIN_CUST_ID);


--doing------Need spaces in the OAP from Mrinal, so create after he adds space overthere----------
CREATE MULTISET TABLE PP_OAP_HARSAGARWAL_T.SNPT_JP_F6781_START_AUD_MP
AS
(
SELECT LATIN_CUST_ID FROM PP_OAP_HARSAGARWAL_T.SNPT_UG_F6781_PRE_AUD_MP A
JOIN PP_DISCOVERY_VIEWS.fact_payment F ON A.LATIN_CUST_ID=F.RCVR_ID
WHERE pmt_success_dt > current_date() -  370
) WITH DATA PRIMARY INDEX(LATIN_CUST_ID);


create  table  PP_OAP_HARSAGARWAL_T.SNPT_SK_pmt_flow_key as 
( select pmt_flow_key2 from  pp_access_views.cdim_payment_flow2 c Where c.primary_flow not like '%DIRECT%' and (c.flow_family in  ('MS FF EC A La Carte','MS FF PayPal Payments Advanced','MS FF PayPal Payments Pro','MS FF PayPal Plus','MS FF Website Payments Standard'))/*where  flow_family IN('MS FF EC A La Carte', 'MS FF Website Payments Standard', 'MS FF PayPal Plus')OR primary_flow like '% EC %' or sub_flow IN ('MS HSS Login','MS HSS Direct Payments','MS Mobile HSS Direct Payments','MS Pro Direct Payments - RP','MS Pro Direct Payments','MS Pro Direct Payments - Gateway Non-BYOB - RP','MS Pro Direct Payments - Gateway Non-BYOB','MS PPA Direct Payments', 'MS PPA Direct Payments - Swipe','MS PPPlus EC A La Carte Mark - Hermes','MS PPPlus EC A La Carte Mark','MS PPPlus Mobile EC A La Carte Mark - Hermes') */group by 1)
with data unique primary index (pmt_flow_key2) ;

Create table PP_OAP_HARSAGARWAL_T.SNPT_SK_KORE_Partner_Map as
(
	sel	distinct a.prtnr_sf_acct_id, a.prtnr_name, b.Is_MarketPlace 
	from	pp_access_views.dim_prtnr_all a
	join
	(
		sel	distinct prtnr_sf_Acct_id, 'Shopping Cart' as Is_MarketPlace  
		from	pp_access_views.dim_prtnr_all
		where	prtnr_name like any (
		'%Shopify%',
		'%Big Commerce%',
		'%WooCommerce%',
		'%Wix%',
		'%EKM%',
		'%Opencart%',
		'%Ecwid%')
		group by 1,2 
		
		union
		
		sel	distinct prtnr_sf_Acct_id, 'Market Place' as Is_MarketPlace  
		from	pp_access_views.dim_prtnr_all
		where	prtnr_name like any (
		'%Etsy%',
		'%Shpock%',
		'%Depop%',
		'%Twickets%',
		'%ASOS Marketplace %',
		'%Big Cartel %')
		group by 1,2) b
		on a.prtnr_sf_Acct_id = b.prtnr_sf_Acct_id
	where	a.currently_active_flag = 'Y' 
	group by 1,2,3
) 
with data 
unique primary index (prtnr_sf_acct_id);


create multiset table PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_Part_XO_KORE_Test  as ( with raw as ( 	select	fpd.pmt_sent_txnid ,	fpd.cal_dt,	fpd.rcvr_id,	xclick_button_src,	sum(success_Cnt) as success_Cnt,	sum(fpd.ntpv_usd_amt) as ntpv	from	pp_discovery_views.fact_payment_detail fpd 	where	cal_dt between current_date-2 		and current_date-1		and success_Cnt > 0		and is_pmt_official_y_n = 'Y'		and rcvr_cntry_code in ('GB')		and pmt_flow_key in ( 		select	pmt_flow_key2 		from	PP_OAP_HARSAGARWAL_T.SNPT_SK_pmt_flow_key ) 	group by 1,2,3,4) select	distinct raw.rcvr_id,d.Is_MarketPlace,min(cal_dt) as cal_Dt from	raw join PP_ACCESS_VIEWS.dim_sf_acct_bn_code_lnk bn	on trim(xclick_button_src) = trim(bn.bn_code) 	and raw.cal_dt between bn.lnk_strt_dt 	and bn.lnk_end_dt join PP_OAP_HARSAGARWAL_T.SNPT_SK_KORE_Partner_Map d 	on bn.acct_id = d.prtnr_sf_acct_id group by 1,2) with data unique primary index (rcvr_id,Is_MarketPlace );


create multiset table PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_Part_XO_KORE_Test_ebay  as ( 

with raw as ( 
	select
	fpd.pmt_sent_txnid ,
	fpd.cal_dt,
	fpd.rcvr_id,
	xclick_button_src,
	sum(success_Cnt) as success_Cnt,
	sum(fpd.ntpv_usd_amt) as ntpv
	from	pp_discovery_views.fact_payment_detail fpd 
	where	cal_dt between current_date-2 
		and current_date-1
		and success_Cnt > 0
		and is_pmt_official_y_n = 'Y'
		and rcvr_cntry_code in ('GB')
		and pmt_flow_key in ( 
		select	distinct pmt_flow_key2 
		from	pp_access_views.cdim_payment_flow2  
		where	 FLOW_FAMILY LIKE 'MP%' ) 
	group by 1,2,3,4) 

select	
distinct 
raw.rcvr_id,
'Market Place' as Is_MarketPlace,
min(cal_dt) as cal_Dt
from	raw 
group by 1,2
) 
with data 
unique primary index (rcvr_id,Is_MarketPlace );

create multiset table PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_MKT_XO_KORE_Test as
(select distinct rcvr_id, Is_MarketPlace, min(cal_dt) as cal_Dt
from 
(select * from PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_Part_XO_KORE_Test

union all

sel * from PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_Part_XO_KORE_Test_ebay ) a
group by 1,2
) with data unique primary index (rcvr_id,Is_MarketPlace );


create multiset table PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_MKT_XO_KORE_Test as
(
	select	distinct rcvr_id, Is_MarketPlace, min(cal_dt) as cal_Dt
	from	
	(
		select	* 
		from	PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_Part_XO_KORE_Test
		
		union all
		
		sel	* 
		from	PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_Part_XO_KORE_Test_ebay ) a
	group by 1,2
) 
with data 
unique primary index (rcvr_id,Is_MarketPlace );

create multiset table PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_Part_XO_KORE_L365_ebay  as ( 

with raw as ( 
	select
	fpd.pmt_sent_txnid ,
	fpd.cal_dt,
	fpd.rcvr_id,
	xclick_button_src,
	sum(success_Cnt) as success_Cnt,
	sum(fpd.ntpv_usd_amt) as ntpv
	from	pp_discovery_views.fact_payment_detail fpd 
	where	cal_dt between current_date-370 
		and current_date-3
		and success_Cnt > 0
		and is_pmt_official_y_n = 'Y'
		and rcvr_cntry_code in ('GB')
		and pmt_flow_key in ( 
		select	distinct pmt_flow_key2 
		from	pp_access_views.cdim_payment_flow2  
		where	 FLOW_FAMILY LIKE 'MP%' ) 
	group by 1,2,3,4) 

select	
distinct 
raw.rcvr_id,
'Market Place' as Is_MarketPlace,
min(cal_dt) as cal_Dt
from	raw 
group by 1,2
) 
with data 
unique primary index (rcvr_id,Is_MarketPlace );

create multiset table PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_Part_XO_KORE_L365_F as (
	select	distinct rcvr_id,
			Is_MarketPlace,
			min(cal_dt) as cal_Dt 
	from	 (
		select	* 
		from	PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_Part_XO_KORE_L365 
		union all 
		sel	* 
		from	PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_Part_XO_KORE_L365_ebay ) a 
	group by 1,2 ) 
with data 
unique primary index (rcvr_id,
		Is_MarketPlace );
		

create  table PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_Part_XO_KORE_L365_Final as
(
	Sel	rcvr_id, Is_MarketPlace 
	from	PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_MKT_XO_KORE_Test a 
	where	rcvr_id ||'-'|| Is_MarketPlace not in (
		Select	distinct rcvr_id ||'-'|| Is_MarketPlace 
		from	PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_Part_XO_KORE_L365_F) 
	group by 1,2
)
with data 
primary index(rcvr_id,Is_MarketPlace );


create multiset table PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_Part_XO_KORE_5D_Test  as ( 

with raw as ( 
	select
	fpd.pmt_sent_txnid ,
	fpd.cal_dt,
	fpd.rcvr_id,
	xclick_button_src,
	sum(success_Cnt) as success_Cnt,
	sum(fpd.ntpv_usd_amt) as ntpv
	from	pp_discovery_views.fact_payment_detail fpd 
	where	cal_dt between current_date-195 
		and current_date-1
		and success_Cnt > 0
		and is_pmt_official_y_n = 'Y'
		and rcvr_cntry_code in ('GB')
		and pmt_flow_key in ( 
		select	pmt_flow_key2 
		from	PP_OAP_HARSAGARWAL_T.SNPT_SK_pmt_flow_key ) 
	group by 1,2,3,4) 

select	
distinct 
raw.rcvr_id,
d.Is_MarketPlace,
min(cal_dt) as cal_Dt
from	raw 
join PP_ACCESS_VIEWS.dim_sf_acct_bn_code_lnk bn
	on trim(xclick_button_src) = trim(bn.bn_code) 
	and raw.cal_dt between bn.lnk_strt_dt 
	and bn.lnk_end_dt
join PP_OAP_HARSAGARWAL_T.SNPT_SK_KORE_Partner_Map d 
	on bn.acct_id = d.prtnr_sf_acct_id 
group by 1,2
) 
with data 
unique primary index (rcvr_id,Is_MarketPlace );


create multiset table PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_Part_XO_KORE_Test_5D_ebay  as ( 

with raw as ( 
	select
	fpd.pmt_sent_txnid ,
	fpd.cal_dt,
	fpd.rcvr_id,
	xclick_button_src,
	sum(success_Cnt) as success_Cnt,
	sum(fpd.ntpv_usd_amt) as ntpv
	from	pp_discovery_views.fact_payment_detail fpd 
	where	cal_dt between current_date-195 
		and current_date-1
		and success_Cnt > 0
		and is_pmt_official_y_n = 'Y'
		and rcvr_cntry_code in ('GB')
		and pmt_flow_key in ( 
		select	distinct pmt_flow_key2 
		from	pp_access_views.cdim_payment_flow2  
		where	 FLOW_FAMILY LIKE 'MP%' ) 
	group by 1,2,3,4) 

select	
distinct 
raw.rcvr_id,
'Market Place' as Is_MarketPlace,
min(cal_dt) as cal_Dt
from	raw 
group by 1,2
) 
with data 
unique primary index (rcvr_id,Is_MarketPlace );	


create multiset table PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_MKT_XO_KORE_5D_Test as(select distinct rcvr_id, Is_MarketPlace, min(cal_dt) as cal_Dtfrom (select * from PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_Part_XO_KORE_5D_Testunion allsel * from PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_Part_XO_KORE_Test_5D_ebay ) agroup by 1,2) with data unique primary index (rcvr_id,Is_MarketPlace );


create table PP_OAP_HARSAGARWAL_T.SNPT_JP_F6781_LAST_TRX_MP_RCVD as ( sel rcvr_id, max(cal_dt) as last_TRX_dt from PP_OAP_HARSAGARWAL_T.SNPT_SK_GB_MKT_XO_KORE_5D_Test where Is_MarketPlace = 'Market Place' group by 1 ) with data primary index (rcvr_id);

------------Need to execute each and every table in above with logic ----------------

                                     





------------------------++++++++++++++++------------------

sel a.cust_id from PP_OAP_MRKISHORE_T_T.UM_suppressed_list_temp_raj_test a
join pp_oap_mrkishore_t_t.SNPT_SK_GB_MKT_XO_KORE_5D_Test b

on a.cust_id = b.rcvr_id
join PP_UNICA_ACCESS_VIEWS.DW_UA_CUST_CONTACT_HISTORY d
on a.cust_id = d.cust_id
JOIN PP_ACCESS_VIEWS.DW_UA_TREATMENT t  
ON t.treatment_pkg_id=d.cntct_pack_id 
join PP_ACCESS_VIEWS.DW_UA_OFFER O 
ON t.treatment_ofr_id=O.ofr_id
join pp_oap_mrkishore_t_t.SNPT_JP_F6781_LAST_TRX_MP_RCVD g
on on a.cust_id = g.rcvr_id

join pp_oap_mrkishore_t_t.SNPT_JP_KORE_MP_RCVD_CNTCT h
on a.cust_id=h.CUSTOMER_ID

-- BR3_PMT_DT
where b.Is_MarketPlace = 'Market Place'
and b.cal_Dt between current_date () - 5 and current_date () - 1 
and d.CMPGN_CODE = '000015821'
and O.ofr_id = 837407
and d.CNTCT_STATUS_ID = 1
and d.CNTCT_HIST_DATE > '2019-09-27'

and h.OFFER_CODE = '000837408'
and g.last_TRX_dt >= h.LST_CONT_DT

-- -BRAVO 1
AND a.CUST_ID NOT IN
		(
--		CUSTOMERS TARGETED IN BRAVO 01 i.e. SEGMENT 1 AND 2 ABOVE
-- seg1 to exclude from
		)
		
	-- -BRAVO 03 EM
AND a.cust_id NOT in
	(
	
	sel d.cust_id from PP_UNICA_ACCESS_VIEWS.DW_UA_CUST_CONTACT_HISTORY d
	
	join pp_oap_mrkishore_t_t.SNPT_SK_GB_MKT_XO_KORE_5D_Test b

	on d.cust_id = b.rcvr_id
	
	JOIN PP_ACCESS_VIEWS.DW_UA_TREATMENT t  
	ON t.treatment_pkg_id=d.cntct_pack_id 
	join PP_ACCESS_VIEWS.DW_UA_OFFER O 
	ON t.treatment_ofr_id=O.ofr_id
	
	where
	
	b.Is_MarketPlace = 'Market Place'
	AND
	b.cal_Dt between current_date () - 5 and current_date () - 1 
	AND
	d.CMPGN_CODE = '000015821'
	AND
	O.ofr_id IN (837411)
	AND
	d.CNTCT_STATUS_ID = 1
	AND
	d.CNTCT_HIST_DATE > '2019-09-27'
	)

		
	-- -BRAVO 2
AND a.CUST_ID NOT IN
		(
--		CUSTOMERS TARGETED IN BRAVO 02 i.e. SEGMENT 3 ABOVE
		)		
	

-- -LAST CONTACT 2 DAYS:
AND a.cust_id NOT in
	(
	sel d.cust_id from PP_UNICA_ACCESS_VIEWS.DW_UA_CUST_CONTACT_HISTORY d
	
	
	JOIN PP_ACCESS_VIEWS.DW_UA_TREATMENT t  
	ON t.treatment_pkg_id=d.cntct_pack_id 
	join PP_ACCESS_VIEWS.DW_UA_OFFER O 
	ON t.treatment_ofr_id=O.ofr_id
	
	
	where
	d.CMPGN_CODE = '000015821'
	AND
	O.ofr_id in (
	837407,
	837409,
	837411,
	837413,
	837415,
	837417,
	837419,
	837421,
	837423
	)
	AND
	d.CNTCT_STATUS_ID  = 1
	AND
	d.CNTCT_HIST_DATE >= current_date () - 2
	)


-- -CH_HO
AND a.cust_id NOT in
	(
	sel d.cust_id from PP_UNICA_ACCESS_VIEWS.DW_UA_CUST_CONTACT_HISTORY d
	
	
	where 
	d.CMPGN_CODE = '000015821'
	AND
	d.CNTCT_HIST_DATE > '2019-09-27'
	AND
	d.CNTCT_STATUS_ID = 2
	AND
	d.CELL_CODE = '000662708'

	)
	
		
-- -DAILY CH:
AND a.CUST_ID NOT IN
	(
	sel cust_id from 
	PP_UNICA_ACCESS_VIEWS.UA_CUST_CNTCT_HIST_DAILY
	where CELLCODE = '000662708'
	)
	

-- -CH Email 03
AND a.cust_id NOT in
(	
	sel d.cust_id from PP_UNICA_ACCESS_VIEWS.DW_UA_CUST_CONTACT_HISTORY d
	
	
	JOIN PP_ACCESS_VIEWS.DW_UA_TREATMENT t  
	ON t.treatment_pkg_id=d.cntct_pack_id 
	join PP_ACCESS_VIEWS.DW_UA_OFFER O 
	ON t.treatment_ofr_id=O.ofr_id
	
	where

	d.CMPGN_CODE = '000015821'
	AND
	d.CNTCT_HIST_DATE > '2019-09-27'
	AND
	O.ofr_id in (
	837411
	)

)
	
	


