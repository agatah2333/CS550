-- Query 1

create view shippedVSCustDemand as
	select c.customer as customer, c.item as item, sum(nvl(s.qty,0)) as suppliedQty, c.qty as demandQty
		from customerDemand c 
		left outer join shipOrders s 
		on c.item = s.item and c.customer = s.recipient
		group by c.customer, c.item, c.qty
		order by c.customer, c.item
		;

		


-- Query 2

create view totalManufItems as 
	select m.item as item, sum(m.qty) as totalManufQty
		from manufOrders m
		GROUP BY m.item
		order by m.item;
		


-- Query 3
-- Reference: Final Exam review, module 14
create view matsUsedVsShippedone as
select m.manuf as manuf , b.matItem as matItem, sum( m.qty * b.QtyMatPerItem) as requiredQty
	from manufOrders m, billOfMaterials b
	where m.item = b.prodItem
	group by m.manuf, b.matItem;

create view matsUsedVsShipped as
	select mu.manuf, mu.matItem, mu.requiredQty, nvl(sum(s.qty),0) as shippedQty
	from matsUsedVsShippedone mu,  shipOrders s 
	where mu.matitem = s.item(+)
    and mu.manuf = s.recipient(+)
	group by mu.manuf, mu.matItem, mu.requiredQty
	order by mu.manuf, mu.matItem
	;


-- Query 4

create view producedVsShipped as
	select	m.item as item, m.manuf as manuf, nvl(sum(s.qty),0) as shippedOutQty, m.qty as  orderedQty
	from manufOrders m, shipOrders s
	where m.item = s.item(+)
    and m.manuf = s.sender(+)
	group by m.item, m.manuf, m.qty
	order by m.item, m.manuf
	;

-- Query 5
create view suppliedVsShipped as
	select	s.item as item, s.supplier as supplier, s.qty  as suppliedQty, nvl(sum(sh.qty),0) as shippedQty
	from supplyOrders s, shipOrders sh
	where s.item = sh.item(+)
    and s.supplier = sh.sender(+)
	group by s.item, s.supplier, s.qty
	order by s.item, s.supplier
	;



-- Query 6
create view view1 as
	select so.supplier , sum( so.qty * s.ppu) as CostBeforeDisc
		from supplyOrders so, supplyUnitPricing s
		where so.item = s.item and so.supplier = s.supplier 
		group by so.supplier;


create view perSupplierCost as
	select sp.supplier,
	nvl((case
	when w.CostBeforeDisc < sp.amt1 then w.CostBeforeDisc
	when w.CostBeforeDisc >sp.amt2 then ((sp.amt1+(sp.amt2-sp.amt1)*(1-sp.disc1))+(w.CostBeforeDisc  - sp.amt2)*(1-sp.disc2))
	when w.CostBeforeDisc >sp.amt1 and w.CostBeforeDisc < sp.amt2 then (sp.amt1+(w.CostBeforeDisc - sp.amt1)*(1-sp.disc1))
	end),0) as cost

	from view1 w, supplierDiscounts sp
	where w.supplier(+) = sp.supplier  
	
	order by sp.supplier
	;


-- Query 7
--manufUnitPricing(manuf, prodItem, setUpCost, prodCostPerUnit): For
--manufacturing of prodItemby manuf, the manufacturer base cost is computedas
--setUpCost plus the prodPricePerUnit times the qty of the produced prodItem 
create view mview1 as
	select mo.manuf , sum (m.setUpCost+( m.prodcostPerUnit * mo.qty)) as CostBeforeDisc
		from manufOrders mo, manufUnitPricing  m
		where mo.item = m.prodItem and mo.manuf = m.manuf 
		group by mo.manuf;


create view perManufCost as
	select sp.manuf,
	nvl((case
	when w.CostBeforeDisc < sp.amt1 then w.CostBeforeDisc
	when w.CostBeforeDisc > sp.amt1  then (sp.amt1+(w.CostBeforeDisc - sp.amt1)*(1-sp.disc1))
	end),0) as cost

	from mview1 w, manufDiscounts sp
	where w.manuf(+) = sp.manuf  
	
	order by sp.manuf
	;



-- Query 8 - from Module 14, exam prep
-- v1 is weight
create view v1 as
	select so.shipper, s.shipLoc as fromloc, r.shipLoc as toloc , sum( so.qty*i.unitWeight) as CostBeforeDisc
		from shipOrders so, busEntities s, busEntities r, items i
		where so.sender = s.entity and so.recipient = r.entity and so.item = i.item 
		group by so.shipper, s.shipLoc, r.shipLoc;


create view perShipperCost as
	select sp.shipper,
	nvl(sum(greatest((case
	when (w.CostBeforeDisc*sp.pricePerLb)<sp.amt1 then (w.CostBeforeDisc*sp.pricePerLb)
	when (w.CostBeforeDisc*sp.pricePerLb)>sp.amt2 then ((sp.amt1+(sp.amt2-sp.amt1)*(1-sp.disc1))+((w.CostBeforeDisc*sp.pricePerLb) - sp.amt2)*(1-sp.disc2))
	when (w.CostBeforeDisc*sp.pricePerLb)>sp.amt1 and (w.CostBeforeDisc*sp.pricePerLb)<sp.amt2 then (sp.amt1+((w.CostBeforeDisc*sp.pricePerLb) - sp.amt1)*(1-sp.disc1))
	end),sp.minPackagePrice)),0) as cost

	from v1 w, shippingPricing sp
	where w.shipper(+) = sp.shipper and 
	w.fromloc(+) = sp.fromloc and 
	w.toloc(+) = sp.toloc
	group by sp.shipper
	order by sp.shipper
	;





-- Query 9
create view SupplierC as
	select sum(ps.cost) as cost
	from perSupplierCost ps;


create view ManufC as
	select sum(pm.cost) as cost
	from perManufCost pm;

create view ShipC as
	select sum(psh.cost) as cost
	from perShipperCost psh;

create view totalCostBreakDown as
	select s.cost as supplyCost, m.cost as manufCost,  shc.cost as shippingCost, (s.cost+m.cost+shc.cost) as totalCost
	from SupplierC s , ManufC m, ShipC shc
	;


-- Query 10
create view cdv1 as
select cd.customer,cd.item, nvl(sum(distinct so.qty),0) as orderedquantity
	from customerDemand cd, shipOrders so
	where cd.customer = so.recipient(+) and cd.item = so.item(+)
	group by cd.customer,cd.item
	order by cd.customer;

create view customersWithUnsatisfiedDemand as
	select distinct v1.customer
	from cdv1 v1,customerDemand cd
	where cd.item = v1.item and cd.customer = v1.customer and (cd.qty > v1.orderedquantity)
	order by v1.customer
	;

-- Query 11
create view v2s as
select spo.supplier as supplier ,spo.item as item, nvl(sum(so.qty),0) as orderedquan
	from supplyOrders spo, shipOrders so
	where spo.supplier = so.sender(+)
	and spo.item = so.item(+)
	group by spo.supplier,spo.item
	order by spo.supplier;

create view suppliersWithUnsentOrders as
	select distinct so.supplier as supplier
	from v2s v2, supplyOrders so
	where  so.item = v2.item and so.supplier = v2.supplier and (so.qty > v2.orderedquan)
	;

-- Query 12
create view vmu1 as
select m.manuf as manuf, bo.matitem as item, sum( m.qty * bo.QtyMatPerItem) as matneed
	from manufOrders m, billOfMaterials bo
	where m.item = bo.prodItem
	group by m.manuf, bo.matitem;

create view vmu22 as 
select m.manuf as manuf, bo.matitem as item
		from manufOrders m, billOfMaterials bo 
		where m.item = bo.prodItem;

create view vmu2 as
select v22.manuf as manuf, v22.item as item, nvl(sum( so.qty),0) as matsneed
	from  vmu22 v22 left outer join shipOrders so on v22.Item = so.item and so.recipient = v22.manuf
	group by v22.manuf, v22.item;


create view manufsWoutEnoughMats as
	select distinct v1.manuf as manuf
	from vmu1 v1, vmu2 v2 
	where v1.manuf = v2.manuf and v1.item = v2.item and (v1.matneed > v2.matsneed)
	order by v1.manuf;


	
-- Query 13
create view v1um as
select m.manuf as manuf, m.item as item, nvl(sum(so.qty),0) as unsentord
	from manufOrders m, shipOrders so
	where m.manuf = so.sender(+) and m.item = so.item(+)
	group by m.manuf,m.item
	order by m.manuf;

create view manufsWithUnsentOrders as
	select distinct m.manuf
	from v1um v1, manufOrders m
	where m.manuf = v1.manuf and m.item = v1.item and m.qty > v1.unsentord
	;