cv = (x) => x.split("\n").map(n => { 
    items = n.split("\t")
    return `"${items[0]}": [${items.slice(1).join(',')}]`
}).join(",\n")

console.log(cv(`Infinity 8 Bali	5	1	5	2	1	2	2	2
Episode Kuta Bali	9	1	5	2	2	2	2	2
Fairfield by Marriott Bali Kuta Sunset Road	10	2	5	2	1	2	2	1
Luminor Hotel Legian Seminyak Bali	8	2	5	2	1	1	2	2
Grandmas Plus Hotel Legian	3	2	5	2	1	1	1	2
Grandmas Plus Hotel Airport	4	1	5	2	1	1	1	2
Choice Stay Hotel Denpasar	5	2	5	2	1	2	2	2
Daun Bali Seminyak Hotel	5	1	5	2	1	1	2	2
Quest San Denpasar by ASTON	4	1	5	2	1	1	1	2
PassGo Digital Airport Hotel Bali	4	2	1	2	1	1	1	2
Yans House Hotel Kuta	4	2	5	2	2	2	2	2
Aralea CoLiving	4	3	5	2	2	1	1	2
Paripadi Studio Canggu	8	3	4	2	1	2	2	2
Kamaniiya Petitenget Seminyak	7	1	5	2	1	1	2	2
Black Lava Camp Kintamani	5	1	5	2	1	1	1	2
Sari Villa Ubud	4	2	4	2	1	1	1	2
Cove Vin Stay Petanu	3	1	3	2	1	1	1	1`))