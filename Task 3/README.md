# Tema 1 - Retele de Calculatoare
**Student: Cristina Ureche** 

## Enuntul temei
Sa se implementeze un server de gestionare produse prin protocol text. 
Serverul trebuie sa mentina in memorie un dictionar: `dic = {"key": value, "key2": value2}`.

### Comenzi obligatorii:
- **ADD** -> param cheie valoare -> raspunde OK - record add
- **GET** -> param cheie -> DATA valoare -> Daca nu exista cheia trebuie dat ERROR invalid key
- **REMOVE** -> param cheie -> OK value deleted -> Gestioneaza erorile

### Comenzi noi:
- **LIST** -> DATA|key=value,key2=value2
- **COUNT** -> DATA Countul elementelor
- **CLEAR** -> sterge tot -> raspuns all data deleted
- **UPDATE** -> param cheie new value -> raspuns Data updated
- **POP** -> param key -> returneaza valoarea si sterge elementul
- **Quit** -> inchide aplicatia

---

## Cum se foloseste 

Am facut serverul sa suporte conexiuni multiple folosind threading. Protocolul e simplu: se trimite comanda, iar serverul raspunde cu lungimea mesajului urmata de continut (ca sa stim cat sa citim din socket).

### Exemple de comenzi:

1. **Adaugare produse:**
   `client> ADD laptop 3500` -> Raspuns: `OK - record add`
   `client> ADD mouse 150` -> Raspuns: `OK - record add`

2. **Verificare lista:**
   `client> LIST` -> Raspuns: `DATA|laptop=3500,mouse=150`

3. **Update si Pop:**
   `client> UPDATE laptop 4000` -> Raspuns: `Data updated`
   `client> POP mouse` -> Raspuns: `DATA 150` (si il sterge)

4. **Erori:**
   `client> GET tastatura` -> Raspuns: `ERROR invalid key`

### Rulare:
- Se porneste mai intai serverul: `python text-tcp-server.py`
- Se deschide unul sau mai multi clienti: `python text-tcp-client.py`