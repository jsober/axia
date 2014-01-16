--[[
--
-- Returns a dictionary of goods sold at a station. Returns nil
-- if not in a station.
--
--]]
function axia:StationItems()
    if GetStationLocation() then
        local items = {}

        for i = 1, GetNumStationMerch() do
            local item = GetStationMerchInfo(i);
            items[i] = {
                item_id   = item.itemid,
                item_name = item.name,
                price     = item.price,
                volume    = item.volume,
            }
        end

        return items
    end
end

--[[
--
-- Sends a report on the current station's items to the server.
-- Does nothing if not in a station.
--
--]]
function axia:StationReport()
    local stationid = GetStationLocation()

    if stationid and GetCurrentStationType() == 0 then
        local data = axia:LocationData(GetCurrentSectorid())

        data['station_id']   = stationid
        data['station_name'] = GetStationName()
        data['faction_id']   = GetStationFaction()
        data['faction_name'] = FactionName[data['faction_id']]
        data['items']        = axia:StationItems()

        axia:ApiRequest(
            'econ/station_report/',
            'POST',
            data,
            --success
            function(data)
                axia:Log(axia.DATA, 'Commerce report set')
            end,
            --failure
            function(data)
                local label = data['label']
                for field, err in pairs(data['errors']) do
                    axia:Log(axia.ERROR, '%s [%s]: %s', { label, field, err })
                end
            end
        );
    end
end

--[[
--
-- Requests a list of the nearest locations selling an item.
--
--]]
function axia:NearestSellLocations(data)
    local item = table.concat(data, ' ')
    local data = { item = item, sid  = GetCurrentSystemid() }

    axia:ApiRequest(
        'econ/nearest_items/',
        'GET',
        data,
        --success
        function(data)
            axia:Log(axia.DATA, 'Closest locations where "%s" is available:', { item })
            for i, loc in ipairs(data['locations']) do
                axia:Log(axia.DATA, loc)
            end
        end,
        --failure
        function(data)
            axia:Log(axia.ERROR, data['error'])
        end
    )
end

--[[
--
-- Requests a list of the cheapest locations selling an item.
--
--]]
function axia:CheapestSellLocations(data)
    local item = table.concat(data, ' ')
    local data = { item = item }

    axia:ApiRequest(
        'econ/cheapest_items/',
        'GET',
        data,
        --success
        function(data)
            axia:Log(axia.DATA, 'Cheapest locations where "%s" is available:', { item })
            for i, loc in ipairs(data['locations']) do
                axia:Log(axia.DATA, loc)
            end
        end,
        --failure
        function(data)
            axia:Log(axia.ERROR, data['error'])
        end
    )
end


--Register events
RegisterEvent(axia.StationReport, 'ENTERED_STATION')

--Register user commands
RegisterUserCommand('find_nearest', axia.NearestSellLocations)
RegisterUserCommand('find_cheapest', axia.CheapestSellLocations)
