import sys
sys.path.append(".")
from RFEM.Loads.surfaceLoad import *
from RFEM.Loads.memberLoad import *
from RFEM.Loads.nodalLoad import *
from RFEM.LoadCasesAndCombinations.loadCase import *
from RFEM.LoadCasesAndCombinations.staticAnalysisSettings import *
from RFEM.TypesForMembers.memberHinge import *
from RFEM.TypesForNodes.nodalSupport import *
from RFEM.BasicObjects.solidSet import *
from RFEM.BasicObjects.surfaceSet import *
from RFEM.BasicObjects.memberSet import *
from RFEM.BasicObjects.lineSet import *
from RFEM.BasicObjects.opening import *
from RFEM.BasicObjects.solid import *
from RFEM.BasicObjects.surface import *
from RFEM.BasicObjects.member import *
from RFEM.BasicObjects.line import *
from RFEM.BasicObjects.node import *
from RFEM.BasicObjects.thickness import *
from RFEM.BasicObjects.section import *
from RFEM.BasicObjects.material import *
from RFEM.initModel import *
from RFEM.dataTypes import *
from RFEM.enums import *

if __name__ == '__main__':

    # Modeling of 2 span beam Fixed at both Ends, intermediate support is Roller support 

    # Create Beam inputs Span, Load
    clientModel.service.begin_modification()

    B1 = float(input('Length of the BEAM in m: '))
    #NS = float(input('location intermediate support in m: '))  # Node 4 
    PL = float(input('Location of Point Load in m: '))         # Node 3

    VL1 = float(input('Varying Load in 1st span start in kN/m: '))  # Varying Load start/End in 1st span kn/m
    VR1 = float(input('Varying Load in 1st span End in kN/m: ')) 

    VL2 = float(input('Varying Load in 2nd span start in kN/m: '))    # Varying Load start/End in 2nd span kn/m
    VR2 = float(input('Varying Load in 2nd span start End in kN/m: '))

    L1S = float(input('Load 1st span Start in m: '))         # Varying Load 1st span Start location in m
    L1E = float(input('Load 1st span1 End in m: '))          # Varying Load 1st span End location in m

    L2S = float(input('Load 2nd span Start in m: '))                   # Varying Load 2nd span Start location in m
    L2E = float(input('Load 2nd End in m: '))                   # Varying Load 2nd span End location in m

    F1 = float(input('Force1 in kN: '))       # Concentrated Load applied @ node 3

    

    # Create Material 
    Material(1, 'S235')

    # Create Thickness
    Section(1, 'IPE 300')
    

    # Create Nodes
    Node(1, 0.0, 0.0, 0.0)
    Node(2, B1, 0.0, 0.0)
    Node(3, PL, 0.0, 0.0)
    #Node(4, NS, 0.0, 0.0)


    # Create Member
    Member(1, MemberType.TYPE_BEAM, '1', '2', 0, 1, 1)
    
    # Create Nodal Supports
    NodalSupport(1, '1', NodalSupportType.HINGED)
    NodalSupport(2, '2', NodalSupportType.ROLLER_IN_X)
    #NodalSupport(4, '4', NodalSupportType.ROLLER_IN_X)
    

    # Create Static Analysis Settings
    StaticAnalysisSettings(1,  StaticAnalysisType.GEOMETRICALLY_LINEAR)

    # Create Load Case
    LoadCase(2, 'IMPOSED', [False])

    # Create Member Load 
    NodalLoad(1, 2, '3', LoadDirectionType.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W, F1*1000)
    MemberLoad.Force(0, 2, 2, '1', MemberLoadDistribution.LOAD_DISTRIBUTION_VARYING, MemberLoadDirection.LOAD_DIRECTION_LOCAL_Z, load_parameter=[[L1S, 0, VL1*1000], [L1E, 0, VR1*1000]])
    MemberLoad.Force(0, 3, 2, '1', MemberLoadDistribution.LOAD_DISTRIBUTION_VARYING, MemberLoadDirection.LOAD_DIRECTION_LOCAL_Z, load_parameter=[[L2S, 0, VL2*1000], [L2E, 0, VR2*1000]])

    Calculate_all()

    print('Ready!')

    clientModel.service.finish_modification()



