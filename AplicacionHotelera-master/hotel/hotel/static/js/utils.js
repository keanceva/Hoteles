function handle_estado()
{
    console.log("Entra a change");
  if (document.getElementById('removed').checked)
  {      
    document.getElementById('is_removed').value = "1";
  } else {
    
    document.getElementById('is_removed').value = "0";
  }
}