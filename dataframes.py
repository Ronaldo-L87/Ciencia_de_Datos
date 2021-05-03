import pandas as pd
## Lectura de los archivos csv
salud_per_capita = pd.read_csv("Presupuesto_Salud_per_capita.csv")
suicidios_vs_desigualdad = pd.read_csv("Suicidios_vs_desigualdad.csv")
salud_mental = pd.read_csv("porcentaje_salud_mental.csv")
tasa_suicidios = pd.read_csv("suicide-death-rates.csv")
desigualdad = pd.read_csv("API_SI.POV.GINI_DS2_en_csv_v2_2252167.csv")
clasificacion = pd.read_csv("Metadata_Country_API_SI.POV.GINI_DS2_en_csv_v2_2252167.csv")
por_causas = pd.read_csv("Numero_muertes_por_causa.csv")
poblacion = pd.read_csv("API_SP.POP.TOTL_DS2_en_csv_v2_2252106.csv")
causas = por_causas
salud = salud_per_capita
suicidios = tasa_suicidios
desigualdad = desigualdad.fillna(0)
salud_per_capita = salud_per_capita.fillna(0)
## Filtrado de datos de suicidios y desigualdad de ingresos
is_filtro = (suicidios["Year"] > 1999) & (suicidios["Year"] < 2018)
suicidios = suicidios[is_filtro]
is_filtro = (causas["Year"] > 1999) & (causas["Year"] < 2018)
causas = causas[is_filtro]
suicidios = suicidios.rename(columns={"Entity":"Country Name"})
causas = causas.rename(columns={"Entity":"Country Name"})
suicidios = suicidios.rename(columns={"Self-harm":"Self-harm share"})
causas = causas[["Country Name", "Year", "Self-harm"]]
filtrado_1 = pd.merge(suicidios, causas, how="inner", on=["Country Name", "Year"])
desigualdad = desigualdad[["Country Name","2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017"]]
clasificacion = clasificacion.rename(columns={"TableName":"Country Name"})
clasificacion = clasificacion[["Country Name", "IncomeGroup"]]
filtrado_2 = pd.merge(desigualdad, clasificacion, how="inner", on="Country Name")
filtrado_2 = pd.melt(filtrado_2, id_vars=["Country Name", "IncomeGroup"], var_name="Year", value_name="Gini index")
lista = list(set(filtrado_1["Country Name"]))
filtro = filtrado_2["Country Name"].isin(lista)
filtrado_2 = filtrado_2[filtro]
filtrado_2 = filtrado_2.sort_values(["Country Name", "Year"], ascending=True)
nueva_lista = list(set(filtrado_2["Country Name"]))
filtro = filtrado_1["Country Name"].isin(nueva_lista)
filtrado_1 = filtrado_1[filtro]
filtrado_1 = filtrado_1.sort_values(["Country Name", "Year"], ascending=True)
filtrado_2 = filtrado_2.sort_values(["Country Name", "Year"], ascending=True)
filtrado_1["Gini index"] = list(filtrado_2["Gini index"])
filtrado_1["Income Group"] = list(filtrado_2["IncomeGroup"])
filtrado_1.to_csv("suicidios_y_desigualdad.csv")
## Filtrado de datos muertes por suicidios y población mundial
filtro = por_causas["Entity"] == "World"
por_causas = por_causas[filtro]
filtro = poblacion["Country Name"] == "World"
poblacion = poblacion[filtro]
poblacion = poblacion[["Country Name", "1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999","2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017"]]
poblacion_2 = pd.melt(poblacion, id_vars=["Country Name"], var_name="Date", value_name="Population")
poblacion_2["Self-harm"] = list(por_causas["Self-harm"])
poblacion_2["Proporcion"] = ((poblacion_2["Self-harm"] ) / poblacion_2["Population"])
#poblacion_2.to_csv("suicidios_vs_poblacion.csv")
## Filtrado de datos muertes por suicidio y nivel de ingreso
#is_filtro = (causas["Year"] > 1999) & (causas["Year"] < 2018)
#causas = causas[is_filtro]
#causas = causas.rename(columns={"Entity":"Country Name"})
#causas = causas.rename(columns={"Code":"Country Code"})
#causas = causas[["Country Name", "Country Code", "Year", "Self-harm"]]
#clasificacion = clasificacion.rename(columns={"TableName":"Country Name"})
#clasificacion = clasificacion[["Country Name", "Country Code","IncomeGroup"]]
#filtrado = pd.merge(clasificacion, causas, how="inner", on="Country Code")
#filtrado.to_csv("prueba.csv")

## Filtrado de datos por tasa de suicidio, gasto de salud y gasto en salud mental
filtro = tasa_suicidios["Year"] == 2011
tasa_suicidios = tasa_suicidios[filtro]
tasa_suicidios = tasa_suicidios.rename(columns={"Entity":"Country Name"})
tasa_suicidios = tasa_suicidios[["Country Name", "Self-harm"]]
salud = salud[["Country Name", "2011"]]
paises2 = pd.merge(salud_mental, salud, how="inner", on="Country Name")
paises3 = pd.merge(paises2, tasa_suicidios, how="inner", on="Country Name")
paises3["Cantidad salud mental"] = paises3["Goverment expenditures on mental health (%)"] * (paises2["2011"]/100)
is_paises = list(paises3["Country Name"])
#paises3.to_csv("salud_mental_per_capita.csv")
