--[[
    Autor: duhack
    GitHub: https://github.com/duhack
    Discord: duhack#9590
]]

function renderAvatar ()
    dxDrawImage(1700, 50, 180, 180, getElementData(localPlayer, "avatar"))
end
addEventHandler ( "onClientRender", root, renderAvatar )

-- Przykładowe zastosowanie: (CIĄG DALSZY ZE STRONY SERVERA)

addEvent("onClientGotImage", true)
addEventHandler("onClientGotImage", resourceRoot,
    function(pixels)
        setElementData(localPlayer, "avatar", dxCreateTexture(pixels))
    end)