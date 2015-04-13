from WMCore.Configuration import Configuration
config = Configuration()

count=0

model = [
'T1bbbb_1500_100',
'T1bbbb_1000_900',
'T1tttt_1500_100',
'T1tttt_1200_800',
'T1qqqq_1400_100',
'T1qqqq_1000_800',
'T2bb_900_100',
'T2bb_600_580',
'T2tt_850_100',
'T2tt_650_325',
'T2tt_500_325',
'T2tt_425_325',
'T2qq_1200_100',
'T2qq_600_550',
]

requestName=model[count]+"_hiJet_mergeHT_sigExpected_v3"
datacard="datacard_"+model[count]+"_hiJet_mergeHT.root"

ArgModel="model="+model[count]
#ArgCount="count="+str(count)

config.section_('General')
config.General.transferLogs=True
#config.General.workArea = 'crab_limits'
config.General.requestName = requestName

config.section_('JobType')
config.JobType.psetName = 'combine_crab_fake_pset.py'
config.JobType.pluginName = 'PrivateMC'
config.JobType.inputFiles = ['libHiggsAnalysisCombinedLimit.so', 'combine', datacard, 'FrameworkJobReport.xml']
config.JobType.outputFiles = ['outputToy.tgz']
config.JobType.scriptExe = 'combine_crab_sig.sh'
config.JobType.scriptArgs = [ArgModel]


config.section_('Data')
#config.Data.inputDataset = 'None'
config.Data.primaryDataset = 'None'
config.Data.outLFN = '/store/user/mmasciov/Signficance_hiJet_mergeHT_Expected_v3/'
config.Data.unitsPerJob = 10
config.Data.splitting = 'EventBased'
config.Data.totalUnits = 100

config.section_('User')

config.section_('Site')
config.Site.storageSite = 'T3_CH_PSI'
#config.Site.whitelist = ['T2_CH_CSCS', 'T2_CH_CERN']
