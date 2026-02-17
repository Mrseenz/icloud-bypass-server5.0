<?php
$serverlist = file(__DIR__ . '/servers.txt', FILE_SKIP_EMPTY_LINES | FILE_IGNORE_NEW_LINES);

$requestlist = '';
foreach (glob(__DIR__ . '/requests/*.xml') as $filename) {
    $base = basename($filename);
    $name = basename($filename, '.xml');
    $requestlist .= '<a href="fake-request.php?file=' . rawurlencode($base) . '">' . htmlspecialchars($name, ENT_QUOTES, 'UTF-8') . '</a><br/>';
}

$ECID = '';
$ICCID = '';
$AppleSerialNumber = '';
$IMEI = '';
$IMEI2 = '';
$IMSI = '';
$activationinfo = '';

$requestFileParam = isset($_GET['file']) ? basename($_GET['file']) : '';
$requestfilename = __DIR__ . '/requests/' . $requestFileParam;

if ($requestFileParam !== '' && file_exists($requestfilename)) {
    $activationinfo = file_get_contents($requestfilename);

    $encodedrequest = new DOMDocument();
    $encodedrequest->loadXML($activationinfo);
    $activationDecoded = base64_decode($encodedrequest->getElementsByTagName('data')->item(0)->nodeValue, true);

    if ($activationDecoded !== false) {
        $decodedrequest = new DOMDocument();
        $decodedrequest->loadXML($activationDecoded);
        $nodes = $decodedrequest->getElementsByTagName('dict')->item(0)->getElementsByTagName('*');

        for ($i = 0; $i < $nodes->length - 1; $i += 2) {
            switch ($nodes->item($i)->nodeValue) {
                case 'UniqueChipID': $ECID = $nodes->item($i + 1)->nodeValue; break;
                case 'IntegratedCircuitCardIdentity': $ICCID = $nodes->item($i + 1)->nodeValue; break;
                case 'SerialNumber': $AppleSerialNumber = $nodes->item($i + 1)->nodeValue; break;
                case 'InternationalMobileEquipmentIdentity': $IMEI = $nodes->item($i + 1)->nodeValue; break;
                case 'InternationalMobileEquipmentIdentity2': $IMEI2 = $nodes->item($i + 1)->nodeValue; break;
                case 'SecondaryInternationalMobileEquipmentIdentity': $IMEI2 = $nodes->item($i + 1)->nodeValue; break;
                case 'InternationalMobileSubscriberIdentity': $IMSI = $nodes->item($i + 1)->nodeValue; break;
            }
        }
    }
}

$initialserver = isset($serverlist[0]) ? $serverlist[0] : 'http://localhost/';
$servers = '';
foreach ($serverlist as $item) {
    $safe = htmlspecialchars($item, ENT_QUOTES, 'UTF-8');
    $servers .= '<option value="' . $safe . '">' . $safe . '</option>';
}

echo '
<html>
<title>IDevice activation</title>
<script type="text/javascript">function changeServer(aForm,aValue){aForm.setAttribute("action",aValue);}</script>
<body>
<form id="request-form" action="' . htmlspecialchars($initialserver, ENT_QUOTES, 'UTF-8') . '" method="POST">
  <p><b>iDevice activation form</b></p>
  <p><input type="submit" value="Activate"></p>
  <p>
        <table>
            <tr>
                <td>
                    <table>
                        <tr><td>SERVER:</td><td><select name="SRVNAME" size=1 required autofocus onChange="changeServer(this.form,this.value);" style="width: 635px">' . $servers . '</select></td></tr>
                        <tr><td>ECID:</td><td><input type="text" size=100 name="ECID" value="' . htmlspecialchars($ECID, ENT_QUOTES, 'UTF-8') . '"></td></tr>
                        <tr><td>MachineName:</td><td><input type="text" size=100 name="machineName" value="ICLOUD"></td></tr>
                        <tr><td>InStoreActivation:</td><td><input type="text" size=100 name="InStoreActivation" value="false"></td></tr>
                        <tr><td>ICCID:</td><td><input type="text" size=100 name="ICCID" value="' . htmlspecialchars($ICCID, ENT_QUOTES, 'UTF-8') . '"></td></tr>
                        <tr><td>GUID:</td><td><input type="text" size=100 name="guid" value="0DFAE16C.6F57B068.B803AFB4.CC724E15.96ED2D9C.BFAF971B.95634B69"></td></tr>
                        <tr><td>Apple serial number:</td><td><input type="text" size=100 name="AppleSerialNumber" value="' . htmlspecialchars($AppleSerialNumber, ENT_QUOTES, 'UTF-8') . '"></td></tr>
                        <tr><td>IMEI-1:</td><td><input type="text" size=100 name="IMEI" value="' . htmlspecialchars($IMEI, ENT_QUOTES, 'UTF-8') . '"></td></tr>
                        <tr><td>IMEI-2:</td><td><input type="text" size=100 name="IMEI2" value="' . htmlspecialchars($IMEI2, ENT_QUOTES, 'UTF-8') . '"></td></tr>
                        <tr><td>IMSI:</td><td><input type="text" size=100 name="IMSI" value="' . htmlspecialchars($IMSI, ENT_QUOTES, 'UTF-8') . '"></td></tr>
                        <tr><td>Activation info:</td><td><textarea name="activation-info" cols="80" rows="15">' . htmlspecialchars($activationinfo, ENT_QUOTES, 'UTF-8') . '</textarea></td></tr>
                        <tr><td></td><td><input type="hidden" name="activation-info-base64" value="' . htmlspecialchars(base64_encode($activationinfo), ENT_QUOTES, 'UTF-8') . '"></td></tr>
                    </table>
                </td>
                <td><div style="overflow:auto;height:500px;width:400px;">' . $requestlist . '</div></td>
            </tr>
        </table>
  </p>
 </form>
</body>
</html>';
?>
