
import codecs
import os
import sys
import time
import traceback

import xml.etree.ElementTree as ET
# import win32con
# import win32evtlog
# import win32evtlogutil
# import winerror
#
#
# # ----------------------------------------------------------------------
# def getAllEvents(server, logtypes, basePath):
#     """
#     """
#     if not server:
#         serverName = "localhost"
#     else:
#         serverName = server
#     for logtype in logtypes:
#         path = os.path.join(basePath, "%s_%s_log.log" % (serverName, logtype))
#         getEventLogs(server, logtype, path)
#
#
# # ----------------------------------------------------------------------
# def getEventLogs(server, logtype, logPath):
#     """
#     Get the event logs from the specified machine according to the
#     logtype (Example: Application) and save it to the appropriately
#     named log file
#     """
#     print
#     "Logging %s events" % logtype
#     log = codecs.open(logPath, encoding='utf-8', mode='w')
#     line_break = '-' * 80
#
#     log.write("\n%s Log of %s Events\n" % (server, logtype))
#     log.write("Created: %s\n\n" % time.ctime())
#     log.write("\n" + line_break + "\n")
#     query_handle = win32evtlog.EvtQuery('System', 1, '*[System[(Level <= 3) and TimeCreated[timediff(@SystemTime) <= 86400000]]]')
#
#     # query_handle = win32evtlog.EvtQuery(
#     #     'C:\Windows\System32\winevt\Logs\Microsoft-Windows-TerminalServices-LocalSessionManager%4Operational.evtx',
#     #     win32evtlog.EvtQueryFilePath)
#     #
#     read_count = 0
#     while True:
#         # read 100 records
#         events = win32evtlog.EvtNext(query_handle, 100)
#         read_count += len(events)
#         # if there is no record break the loop
#         if len(events) == 0:
#             break
#         for event in events:
#             xml_content = win32evtlog.EvtRender(event, win32evtlog.EvtRenderEventXml)
#
#             # parse xml content
#             xml = ET.fromstring(xml_content)
#             # xml namespace, root element has a xmlns definition, so we have to use the namespace
#             ns = '{http://schemas.microsoft.com/win/2004/08/events/event}'
#
#             event_id = xml.find(f'.//{ns}EventID').text
#             level = xml.find(f'.//{ns}Level').text
#             channel = xml.find(f'.//{ns}Channel').text
#             execution = xml.find(f'.//{ns}Execution')
#             process_id = execution.get('ProcessID')
#             thread_id = execution.get('ThreadID')
#             time_created = xml.find(f'.//{ns}TimeCreated').get('SystemTime')
#             print(
#                 f'Time: {time_created}, Level: {level} Event Id: {event_id}, Channel: {channel}, Process Id: {process_id}, Thread Id: {thread_id}')
#
#             user_data = xml.find(f'.//{ns}UserData')
#             # user_data has possible any data
#
#     # hand = win32evtlog.OpenEventLog(server, logtype)
#     # total = win32evtlog.GetNumberOfEventLogRecords(hand)
#     # print
#     # "Total events in %s = %s" % (logtype, total)
#     # flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
#     # events = win32evtlog.ReadEventLog(hand, flags, 0)
#     # evt_dict = {win32con.EVENTLOG_AUDIT_FAILURE: 'EVENTLOG_AUDIT_FAILURE',
#     #             win32con.EVENTLOG_AUDIT_SUCCESS: 'EVENTLOG_AUDIT_SUCCESS',
#     #             win32con.EVENTLOG_INFORMATION_TYPE: 'EVENTLOG_INFORMATION_TYPE',
#     #             win32con.EVENTLOG_WARNING_TYPE: 'EVENTLOG_WARNING_TYPE',
#     #             win32con.EVENTLOG_ERROR_TYPE: 'EVENTLOG_ERROR_TYPE'}
#     #
#     # try:
#     #     events = 1
#     #     while events:
#     #         events = win32evtlog.ReadEventLog(hand, flags, 0)
#     #
#     #         for ev_obj in events:
#     #             the_time = ev_obj.TimeGenerated.Format()  # '12/23/99 15:54:09'
#     #             evt_id = str(winerror.HRESULT_CODE(ev_obj.EventID))
#     #             computer = str(ev_obj.ComputerName)
#     #             cat = ev_obj.EventCategory
#     #             ##        seconds=date2sec(the_time)
#     #             record = ev_obj.RecordNumber
#     #             msg = win32evtlogutil.SafeFormatMessage(ev_obj, logtype)
#     #
#     #             source = str(ev_obj.SourceName)
#     #             if not ev_obj.EventType in evt_dict.keys():
#     #                 evt_type = "unknown"
#     #             else:
#     #                 evt_type = str(evt_dict[ev_obj.EventType])
#     #             log.write("Event Date/Time: %s\n" % the_time)
#     #             log.write("Event ID / Type: %s / %s\n" % (evt_id, evt_type))
#     #             log.write("Record #%s\n" % record)
#     #             log.write("Source: %s\n\n" % source)
#     #             log.write(msg)
#     #             log.write("\n\n")
#     #             log.write(line_break)
#     #             log.write("\n\n")
#     # except:
#     #     print
#     #     traceback.print_exc(sys.exc_info())
#     #
#     # print
#     # "Log creation finished. Location of log is %s" % logPath
#
#
# def get_event_log(request):
#     # if __name__ == "__main__":
#     server = None  # None = local machine
#     logTypes = ["System", "Application", "Security"]
#     getAllEvents(server, logTypes, "C:\downloads")
# #
