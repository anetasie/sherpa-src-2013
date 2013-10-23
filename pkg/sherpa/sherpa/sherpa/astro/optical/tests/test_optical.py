# 
#  Copyright (C) 2007  Smithsonian Astrophysical Observatory
#
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from numpy import arange, array
import sherpa.astro.optical as models
from sherpa.utils import SherpaFloat, SherpaTestCase
from sherpa.models.model import ArithmeticModel


class test_models(SherpaTestCase):

    def test_create_and_evaluate(self):
        x = arange(4500.0,5500.0,1,SherpaFloat)
        count = 0

        for cls in dir(models):
            clsobj = getattr(models, cls)

            if ((not isinstance(clsobj, type)) or
                (not issubclass(clsobj, ArithmeticModel)) or
                (clsobj is ArithmeticModel)):
                continue

            m = clsobj()
            self.assertEqual(type(m).__name__.lower(), m.name)
            count += 1

            out = None
            try:
                out  = m(x)
            except ValueError:
                self.fail("evaluation of model '%s' failed" % cls)

            self.assert_(out.dtype.type is SherpaFloat)
            self.assertEqual(out.shape, x.shape)

        self.assertEqual(count, 24)

    def test_absorptionedge(self):
        standard = array([0.9685065820791976, 0.95830229765390307, 0.94620502980922028, 0.93211041526438487, 0.91593671969204127, 0.89762759643043488, 0.87715461698498132, 0.85451946267808121, 0.8297556658693529, 0.80292979279273347, 0.77414196879224828, 0.74352566091922911, 0.71124665253933783, 0.67750116952066985, 0.64251314710620877, 0.60653065971263342, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.AbsorptionEdge()(x), 1.0e-4)
        
    def test_absorptiongaussian(self):
        standard = array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.AbsorptionGaussian()(x), 1.0e-4)

    def test_absorptionlorentz(self):
        standard = array([0.99999999528164518, 0.99999999344606083, 0.99999999095416015, 0.99999998754059471, 0.99999998280335212, 0.99999997611333014, 0.99999996644725742, 0.99999995206078363, 0.99999992980244812, 0.99999989354214869, 0.99999983013930149, 0.99999970738850019, 0.99999942907991879, 0.99999859599970375, 0.99999388511010501, 0.61834187396562701, 0.99999282351723806, 0.99999806518942824, 0.99999907520469289, 0.99999944198163215, 0.99999961781364088, 0.99999971660402309, 0.9999997781411587, 0.99999981935713333, 0.9999998484884437])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.AbsorptionLorentz()(x), 1.0e-4)

    def test_absorptionvoigt(self):
        standard = array([0.99999999764082259, 0.99999999672303042, 0.99999999547708007, 0.99999999377029736, 0.99999999140167606, 0.99999998805666501, 0.99999998322362871, 0.99999997603039181, 0.999999964901224, 0.99999994677107429, 0.99999991506965069, 0.99999985369425004, 0.99999971453995939, 0.99999929799985188, 0.99999694255505256, 0.8091709369828135, 0.99999641175861897, 0.99999903259471412, 0.99999953760234639, 0.99999972099081602, 0.9999998089068205, 0.99999985830201155, 0.99999988907057935, 0.99999990967856667, 0.9999999242442219])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.AbsorptionVoigt()(x), 1.0e-4)

    def test_accretiondisk(self):
        standard = array([0.25957555738330729, 0.31064956084683815, 0.3594423180313418, 0.40536535443594257, 0.44813629741863797, 0.48767470952984221, 0.52402846787774449, 0.55732327895090761, 0.58772879243423304, 0.61543627632728515, 0.64064420165915337, 0.66354917305466055, 0.68434043714887249, 0.70319676240539508, 0.72028487259128648, 0.73575888234288467, 0.74976036446408467, 0.7624188015556842, 0.7738522578442889, 0.78416816338684248, 0.7934641408355344, 0.80182883053782261, 0.80934268690535582, 0.81607873041955503, 0.82210324718874861])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.AccretionDisk()(x), 1.0e-4)


    def test_blackbody(self):
        standard = array([5.5093731066065929e-05, 0.00030261574279191836, 0.0012047844277601478, 0.0037556134924405268, 0.0096821251257371583, 0.021481901415293728, 0.04225299844834212, 0.075351340732738289, 0.12396794751135611, 0.19072858000961607, 0.27739272840627249, 0.38468894687044297, 0.51228701427059464, 0.65888291892435136, 0.82236141636773319, 1.0, 1.1886834951622101, 1.3851065632514377, 1.5859497062905927, 1.7880215084269324, 1.9883652834123369, 2.1843319853780336, 2.3736234269522005, 2.5543108782765618, 2.7248343372076875])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.BlackBody()(x), 1.0e-4)

    def test_bremsstrahlung(self):
        standard = array([2.4079659661517139e-10, 1.7604071594723798e-09, 9.098981829911976e-09, 3.6061800830879458e-08, 1.1611503710526018e-07, 3.1686751448679294e-07, 7.5639126772929701e-07, 1.6179485975450024e-06, 3.159743691835483e-06, 5.7174095578719225e-06, 9.6985138321704389e-06, 1.5569850435718279e-05, 2.3839321754400511e-05, 3.5034699800776941e-05, 4.9681553818275163e-05, 6.828229834607794e-05, 9.1297812146291763e-05, 0.00011913253630814131, 0.00015212346685498836, 0.00019053305949024319, 0.0002345457764809851, 0.00028426782256692207, 0.00033972952186994742, 0.00040088976076737214, 0.00046764194259725072])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.Bremsstrahlung()(x), 1.0e-4)


    def test_brokenpowerlaw(self):
        standard = array([0.91244353655548083, 0.92118162761253997, 0.92923192839748614, 0.93669959911720135, 0.94366707528673943, 0.95020021650567643, 0.956352499790037, 0.96216796084718881, 0.96768330770414812, 0.97292947195209667, 0.97793276854292854, 0.98271577727617154, 0.98729802265111022, 0.99169650515237262, 0.99592612139785064, 1.0, 0.99608560996092077, 0.99233343506820282, 0.98873110652218021, 0.98526759908204797, 0.98193304456191266, 0.97871857647842575, 0.9756161998234445, 0.97261868125056994, 0.96971945596200482])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.BrokenPowerlaw()(x), 1.0e-4)


    def test_ccm(self):
        standard = array([1.1968507602596983, 4.992714925154532, 20.488597096040085, 80.623723081143211, 299.72850441011815, 1044.8164459402537, 3405.6511209548571, 10382.422581726778, 29661.723255017718, 79650.483812978084, 201739.06329411248, 483728.17792427196, 1102109.6966427318, 2394500.3194501237, 4977948.6996672535, 9933904.9444035497, 19086064.048076943, 35402671.653966099, 63559742.38307213, 110705499.95744966, 187468752.2754392, 309254496.5398131, 497868566.00461102, 783509483.44309497, 1207159931.4463139])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.CCM()(x), 1.0e-4)


    def test_emissiongaussian(self):
        standard = array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.EmissionGaussian()(x), 1.0e-4)

    def test_emissionlorentz(self):
        standard = array([8.8460119073676202e-05, 9.4777130118516213e-05, 0.00010206572915164181, 0.00011056874281047025, 0.0001206172704253954, 0.00013267480502526357, 0.00014741075698717604, 0.00016582909646742654, 0.00018950720602976787, 0.00022107344756576336, 0.0002652574112728564, 0.00033151416988311613, 0.00044189096531537902, 0.00066245299741466454, 0.0013226106060784417, 0.38170761273895537, 0.0013226106060784417, 0.00066245299741466454, 0.00044189096531537902, 0.00033151416988311613, 0.0002652574112728564, 0.00022107344756576336, 0.00018950720602976787, 0.00016582909646742654, 0.00014741075698717604])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.EmissionLorentz()(x), 1.0e-4)

    def test_emissionvoigt(self):
        standard = array([2.9493539159312757e-08, 3.3857378749894552e-08, 3.9266545212663451e-08, 4.6083652933497467e-08, 5.4843354298635128e-08, 6.6360456699082159e-08, 8.1926486410991892e-08, 1.0368820345249175e-07, 1.3542947896188593e-07, 1.8433454496972647e-07, 2.6544168835398889e-07, 4.1475247581613886e-07, 7.3733711165262667e-07, 1.6590044953853394e-06, 6.6359314568841271e-06, 0.38170761273895537, 6.6359314568841271e-06, 1.6590044953853394e-06, 7.3733711165262667e-07, 4.1475247581613886e-07, 2.6544168835398889e-07, 1.8433454496972647e-07, 1.3542947896188593e-07, 1.0368820345249175e-07, 8.1926486410991892e-08])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.EmissionVoigt()(x), 1.0e-4)


    def test_logabsorption(self):
        standard = array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.99999999999999845, 0.99999999999989553, 0.99999999999314593, 0.99999999955228625, 0.99999997087766357, 0.99999811360757984, 0.99987832641225127, 0.99221417691218039, 0.60653065971263342, 0.99218187628563914, 0.9998762867687695, 0.99999804170689144, 0.99999996887513298, 0.99999999950326168, 0.99999999999203959, 0.99999999999987188, 0.99999999999999789, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])

        x = arange(4500.0,5500.0,5,SherpaFloat)

        self.assertEqualWithinTol(standard, models.LogAbsorption()(x), 1.0e-4)

    def test_logemission(self):
        standard = array([2.7283694245522508e-191, 2.771474837013682e-187, 2.7583175501994464e-183, 2.6899385973079625e-179, 2.5706574914813807e-175, 2.4076231954040374e-171, 2.2101091723259581e-167, 1.9886485625458148e-163, 1.7541204390483122e-159, 1.5168950463807105e-155, 1.2861270361020121e-151, 1.0692558226689427e-147, 8.7173758383954736e-144, 6.9700041477750503e-140, 5.4658777454438393e-136, 4.204386738254668e-132, 3.1724682930913117e-128, 2.348440721313834e-124, 1.705631289330599e-120, 1.2154840931626593e-116, 8.499768263798859e-113, 5.8330198570258424e-109, 3.9286473778772586e-105, 2.5971098022414737e-101, 1.6852698957822004e-97, 1.0735308058005487e-93, 6.7136585362820932e-90, 4.1222777933435167e-86, 2.4853176148112904e-82, 1.4713850445847043e-78, 8.5546752055685138e-75, 4.8847934851997723e-71, 2.7395985437445495e-67, 1.5092390096751586e-63, 8.1675468210249678e-60, 4.3422987456787449e-56, 2.2681614450332186e-52, 1.1640884332431931e-48, 5.8706620734046207e-45, 2.9094335939175392e-41, 1.4170365226939782e-37, 6.7832159976707165e-34, 3.1915587920671772e-30, 1.4760907447671419e-26, 6.7111429850971093e-23, 2.9997370734101212e-19, 1.3182658719418509e-15, 5.696205153242e-12, 2.4202516624379408e-08, 0.00010112465244553034, 0.41553184258022047, 0.00010281993407383567, 2.5866747081212425e-08, 6.6155990130809951e-12, 1.7200098735954321e-15, 4.5456797126622994e-19, 1.2210817353375947e-22, 3.3338088892926676e-26, 9.2503665844749366e-30, 2.6083859142451258e-33, 7.4739803319206564e-37, 2.1760654887412815e-40, 6.4373147270475887e-44, 1.9347431524782372e-47, 5.9074610757107171e-51, 1.832359699784315e-54, 5.7733302230557731e-58, 1.8476577059118167e-61, 6.005786462107792e-65, 1.9826472719938647e-68, 6.6469487357298397e-72, 2.2629489391057569e-75, 7.8230684741372112e-79, 2.7460219573643723e-82, 9.7865601148111109e-86, 3.541034479478995e-89, 1.3007063118329874e-92, 4.8501198121898389e-96, 1.8357987829684186e-99, 7.0529772607878094e-103, 2.7502376866834852e-106, 1.0884136895216374e-109, 4.3713904842664952e-113, 1.7816525167441313e-116, 7.3685204901290366e-120, 3.0922008631653204e-123, 1.3166233967864213e-126, 5.687722505693779e-130, 2.4927275450228204e-133, 1.1082750571041181e-136, 4.9984289112479011e-140, 2.2867026991768415e-143, 1.0610925111775114e-146, 4.9939181287946491e-150, 2.3837000151722525e-153, 1.1538817536776669e-156, 5.6643251478386733e-160, 2.8196160009855067e-163, 1.4231954990351101e-166, 7.2836650005050336e-170])
        
        x = arange(4500.0,5500.0,10,SherpaFloat)

        self.assertEqualWithinTol(standard, models.LogEmission()(x), 1.0e-4)

    def test_opticalgaussian(self):
        standard = array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.OpticalGaussian()(x), 1.0e-4)

    def test_polynomial(self):
        standard = array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.Polynomial()(x), 1.0e-4)


    def test_powerlaw(self):
        standard = array([1.5811388300841895, 1.507556722888818, 1.4433756729740643, 1.3867504905630728, 1.3363062095621219, 1.2909944487358056, 1.25, 1.2126781251816647, 1.1785113019775793, 1.1470786693528088, 1.1180339887498949, 1.091089451179962, 1.0660035817780522, 1.0425720702853738, 1.0206207261596576, 1.0, 0.98058067569092011, 0.96225044864937626, 0.94491118252306805, 0.9284766908852593, 0.9128709291752769, 0.89802651013387447, 0.88388347648318444, 0.8703882797784892, 0.85749292571254421])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.Powerlaw()(x), 1.0e-4)


    def test_recombination(self):
        standard = array([3.4836898079341162e-06, 2.5515595256742181e-05, 0.00013208542972397409, 0.00052417470290180347, 0.001689673181710789, 0.0046154368699276036, 0.011026808941925453, 0.023604401096446872, 0.046128458454485585, 0.083516984889125276, 0.14174680201470705, 0.2276685002553003, 0.34874155329896966, 0.5127230768258606, 0.7273437999518656, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.Recombination()(x), 1.0e-4)

    def test_xgal(self):
        standard = array([0.45362998107841551, 0.48531971499295679, 0.51374431755758665, 0.53934148104419477, 0.56248528117315533, 0.58349346983029016, 0.60263554465304658, 0.62014032063345181, 0.63620256636475558, 0.65098863139049556, 0.66464113845055239, 0.67728286375884705, 0.68901993487188196, 0.69994446480494277, 0.71013672453693721, 0.71966693906878776, 0.7285967768297269, 0.73698058910164777, 0.7448664452668764, 0.75229700084357243, 0.75931022814657068, 0.76594003369538621, 0.77221678191538912, 0.77816774101572561, 0.78381746399277263])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.XGal()(x), 1.0e-4)

    def test_fm(self):
        standard = array([0.067920363261718505, 0.014883834789685302, 0.093583048485031503, 0.14450241163673896, 0.16381443353322345, 0.17310368226967346, 0.17857921385701581, 0.18228140664065329, 0.18502333095786874, 0.18718236816043671, 0.18895563246766889, 0.19045613837210473, 0.19175372495742887, 0.19289426720917469, 0.193909448486905, 0.19482207617721881, 0.19564914231668859, 0.19640367416526688, 0.1970959017091056, 0.19773402213493194, 0.19832471706005311, 0.19887351274957324, 0.19938503749637584, 0.19986320975624491, 0.20031137848153305])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.FM()(x), 1.0e-4)

    def test_lmc(self):
        standard = array([0.017972538871898092, 0.018346744475981214, 0.029767112605273569, 0.044404104611715123, 0.057217299818695562, 0.068414886799900612, 0.078456414872706645, 0.087600371084058923, 0.095993790222797012, 0.10986927225335642, 0.12537203637011013, 0.14109275585384703, 0.15692145737419114, 0.17276663958745922, 0.18855300480852619, 0.20421925145657874, 0.2197160309302704, 0.23500411521711256, 0.25005278757846094, 0.26483844955117647, 0.27934342763482517, 0.29355495874176524, 0.307464332457073, 0.32106616893565659, 0.33435781296527223])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.LMC()(x), 1.0e-4)

    def test_sm(self):
        standard = array([0.018879913490962935, 0.012129732955288073, 0.025280421678758935, 0.043433434825655801, 0.061320569217587453, 0.07434662550638331, 0.087995296596485278, 0.10210478729283859, 0.11278447505267959, 0.12243556052032273, 0.13182567385564067, 0.1415976026908683, 0.15110837579811739, 0.16699570978177911, 0.1832158167557246, 0.19952623149688792, 0.21586788386259259, 0.23219005873816106, 0.24757927436115154, 0.26202626575753363, 0.27626974913629299, 0.29029443451503267, 0.30408850256762793, 0.31764307668623049, 0.3309517682878827])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.SM()(x), 1.0e-4)

    def test_smc(self):
        standard = array([0.052966344389165781, 0.082843963674633828, 0.13446104780518578, 0.17967542788895557, 0.23775105293132306, 0.29785164294291888, 0.36698967525684201, 0.40596508880206622, 0.44407159193115886, 0.49226106700577088, 0.5528043203957056, 0.61397354680474936, 0.674775832572302, 0.73527179728742198, 0.79547938777224692, 0.8552153192960873, 0.91433016483910434, 0.97270339853697996, 1.0320821946296628, 1.0923072785937731, 1.1516839999395072, 1.2101486194115134, 1.2676518658578455, 1.3241567354180939, 1.3796365960458694])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.SMC()(x), 1.0e-4)

    def test_seaton(self):
        standard = array([0.030095391688732012, 0.027909500640285866, 0.025100394977664191, 0.022251584751417093, 0.019623917720542776, 0.017307017077863505, 0.01530894675272264, 0.013603387170182283, 0.012152701746359603, 0.010918441834061621, 0.009865634005430321, 0.0089641256727816254, 0.0081886204908309841, 0.00751819215570381, 0.0069356441986238504, 0.0064268771731701936, 0.0059803259055699731, 0.0055864838288276581, 0.0052375116259592161, 0.0049269199409981432, 0.0046493141160051776, 0.0044001895366558453, 0.0041757676757055665, 0.0039728646081619726, 0.0037887853374843675])

        x = arange(2000.0,7000.0,200,SherpaFloat)

        self.assertEqualWithinTol(standard, models.Seaton()(x), 1.0e-4)
