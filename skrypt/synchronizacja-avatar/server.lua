--[[
    Autor: duhack
    GitHub: https://github.com/duhack
    Discord: duhack#9590
]]

-- Przykładowe zastosowanie:
-- !! pamiętaj, aby dodać do ACL admin obiekt: resource.synchronizacja-avatar !!

--konfiguracja
local testoweUID = "1"

local host = "" -- host
local db = "" -- baza danych
local user = "" -- uzytkownik
local password = "" --haslo


-- połączenie z bazą danych
function connect()
    DBConnection = dbConnect( "mysql", "dbname="..db..";host="..host..";charset=utf8", user, password )
    if (not DBConnection) then
        outputDebugString("Blad: Nie udalo sie polaczyc z baza danych!")
    else
        outputDebugString("Sukces: Polaczono z baza danych!")
    end
end
addEventHandler("onResourceStart",resourceRoot, connect)

-- pobranie pobranie avatara
function plrJoin()
    local downloadAvatar = dbQuery(DBConnection, "SELECT * FROM `synchronizacja-dsc` WHERE uid='"..testoweUID.."'")
    local result, num_affected_rows = dbPoll( downloadAvatar, -1 )
    if not(num_affected_rows > 0) then
        outputChatBox("konto nie jest polaczone")
    else
        for i,row in ipairs (result) do
            fetchRemote(row['avatar'], ImageCallback, "", false, source)
        end
    end
end
addEventHandler("onPlayerJoin", root, plrJoin)

-- zapisanie avatara w elementdacie (ciąg dalszy w client side)
function ImageCallback(responseData, error, playerToReceive)
    if error == 0 then
        triggerClientEvent( playerToReceive, "onClientGotImage", resourceRoot, responseData )
    else
        outputChatBox(error)
    end
end