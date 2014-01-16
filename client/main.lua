--[[
--
-- Axia Data Services
--
-- Author: Jeff Ober <jeffober@gmail.com>
--
-- SERVICES
--
-- The following services are provided:
--   * Report ion storms (automatic)
--   * Report obstacles (automatic)
--   * Navigate around ion storms and other obstacles
--   * Provide a list of recently reported ion storms
-- 
-- NAVIGATION
--
-- When an ion storm is encountered, it is automatically reported to the
-- server. No other information beyond the location of the storm is sent.
--
-- To plot your way around known storms, set your destination and waypoints in
-- the navigation system, then use the command "/plot". The plugin will contact
-- the server to get a path clear of known storms.
--
-- To view a list of recently reported ion storms, use the command "/storms".
--
--]]

declare('axia', {})

axia.DATA  = 0
axia.ERROR = 1
axia.WARN  = 2
axia.INFO  = 3
axia.DEBUG = 4

axia.version   = '0.8'
axia.log_level = axia.INFO
axia.base_url  = 'http://axia.artfulcode.net/vo/'
--axia.base_url  = 'http://localhost:8000/vo/'

--Load libraries
dofile('net/tcpsock.lua')
dofile('net/httplib.lua')
dofile('net/json.lua')
dofile('util.lua')
dofile('nav.lua')
dofile('commerce.lua')
