<?php 
$output=null;
$retval=null;

if (isset($_FILES['fichier'])) {
  //echo "tafa";
  $dossier = '/var/www/html/image/';
  $fichier = basename($_FILES['fichier']['name']);
  $taille = filesize($_FILES['fichier']['tmp_name']);
  $extensions = array('.png', '.gif', '.jpg', '.jpeg', '.pdf');
  $extension = strrchr($_FILES['fichier']['name'], '.');
  $nom_image = $_FILES['fichier']['name'];
  //Début des vérifications de sécurité...
  if (!in_array($extension, $extensions)) //Si l'extension n'est pas dans le tableau
  {
    $erreur = 'Vous devez uploader un fichier de type png, gif, jpg, jpeg, txt ou doc';
  }
  if (!isset($erreur)) {
    //S'il n'y a pas d'erreur, on upload
    //On formate le nom du fichier ici...
    $fichier = 'file' . $extension;
    $fichier = preg_replace('/([^.a-z0-9]+)/i', '-', $fichier);
    if (move_uploaded_file($_FILES['fichier']['tmp_name'], $dossier . $fichier)) //Si
    {
      $command = 'python /var/www/html/Modele.py ';
      exec($command, $output, $retval);
      //var_dump($output);
      //header('location:../pages/index.php?out='.$output);
    }
  }
}
?>
<p>La solution de l'equation est : </p>
<p><?php print_r($output); ?></p>