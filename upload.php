<?php
if (isset($_FILES['fichier'])) {
  //echo "tafa";
  $dossier = '../uploads/';
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
    $fichier = preg_replace('/([^.a-z0-9]+)/i', '-', $fichier);
    if (move_uploaded_file($_FILES['fichier']['tmp_name'], $dossier . $fichier)) //Si
    {
      $command = 'python python/prediction_equation.py';
      $output = exec($command);
      //var_dump($output);
      //header('location:../pages/index.php?out='.$output);
    }
  }
}
?>
<p style="text-align: center;"> <?php var_dump ($output); ?> </p>
