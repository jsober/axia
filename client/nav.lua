--[[
--
-- Returns a system id, x, and y coordinates for a given sector id.
--
--]]
function axia:GetSectorCoordinates(sector_id)
    local s, x, y = SplitSectorID(sector_id)
    x = x  - 1
    y = 16 - y
    return s, x, y
end

--[[
--
-- Returns a hash of sid (system id), x, and y coordinates for a given
-- sector_id.
--
--]]
function axia:LocationData(sector_id)
    local sid, x, y = axia:GetSectorCoordinates(sector_id)
    return {
        sid = sid,
        x   = x,
        y   = y,
    }
end

--[[
--
-- On entering a sector with an ion storm, notifies ADS of its presence.
--
--]]
function axia:OnEnterSector(event, data)
    local has_storm     = IsStormPresent()
    local has_obstacles = not axia:IsEmptySector()

    local data = axia:LocationData(GetCurrentSectorid())
    data['has_storm']     = has_storm
    data['has_obstacles'] = has_obstacles

    axia:ApiRequest('nav/sector_report/', 'POST', data,
        -- success handler
        function(data)
            if has_storm then
                axia:Log(axia.DATA, 'Ion storm reported')
            end
        end,
        -- error handler
        function(data)
            for field, err in pairs(data['errors']) do
                axia:Log(axia.ERROR, '%s: %s', { field, err })
            end
        end
    )
end

--[[
--
-- Returns a list of triples for sectors on the currently mapped navigation route
-- in the format:
--   {
--      { system_id, x, y },
--      ...
--   }
--
--]]
function axia:GetCurrentRoute()
    local s, x, y = axia:GetSectorCoordinates(GetCurrentSectorid())
    local sectors = { { s, x, y } }

    for i, v in ipairs(NavRoute.GetCurrentRoute()) do
        local s, x, y = axia:GetSectorCoordinates(v)
        sectors[i + 1] = { s, x, y }
    end

    return sectors
end

--[[
--
-- Re-maps the currently mapped nav route to avoid known storms.
--
--]]
function axia:PlotRoute(args)
    local route    = axia:GetCurrentRoute()
    local data     = { strategy='safe' }

    if #route == 1 then
        OpenAlarm('Navigation Error', 'No route is selected in your navigation computer', 'OK')
        return
    end

    data['route'] = route

    if args then
        data['strategy'] = args[1]
    end

    axia:ApiRequest('nav/plot/', 'GET', data,
        -- success
        function(data)
            local route = data['route']
            if #route > 0 then
                for i, sector_id in ipairs(route) do
                    axia:Log(axia.DEBUG, 'Plotting waypoint %s', { LocationStr(sector_id) })
                end
                NavRoute.clear()
                NavRoute.SetFullRoute(route)
                axia:Log(axia.DATA, 'Plotting complete')
            end
        end,

        -- failure
        function(data)
            axia:Log(axia.ERROR, data['error'])
        end
    )
end

--[[
--
-- Emits a list of known ion storms reported in the last 12 hours.
--
--]]
function axia:ListStorms()
    axia:ApiRequest('nav/storms/', 'GET', nil,
        -- success
        function(data)
            local storms = data['storms']
            axia:Log(axia.DATA, 'Ion storms reported in the last 12 hours:')
            for i, sector_id in ipairs(storms) do
                axia:Log(axia.DATA, '  * %s', { LocationStr(sector_id) })
            end
        end,

        -- failure
        function(data)
            axia:Log(axia.ERROR, data['error'])
        end
    )
end

--[[
--
-- Register event handlers
--
--]]
RegisterEvent(axia.OnEnterSector, 'SECTOR_LOADED')

--[[
--
-- Register bind-able user functions
--
--]]
RegisterUserCommand('plot', axia.PlotRoute)
RegisterUserCommand('storms', axia.ListStorms)

