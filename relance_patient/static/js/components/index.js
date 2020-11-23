
const pathName = window.location.pathname
const domContainer = document.querySelector('#breadcrumb');
const cardBox = document.querySelector("#count-patient")
let items = []



switch (pathName) {
    case "/users/":
        items = [{name: "Accueil", link: "/"}, {name: "Liste des utilisateurs", link: ""}]
        break;

    case "/users/create/":
        items = [{name: "Accueil", link: "/"}, {name: "Liste des utilisateurs", link: "/users/"}, {name: "Création d'utilisateur", link: "/users/"}]
        break;

    // PATIENT LISTING

    case "/patient-listing/":
        items = [{name: "Accueil", link: "/"}, {name: "Listing des patients", link: ""}]
        break;

    case "/patient-listing/all-patients/":
        items = [{name: "Accueil", link: "/"}, {name: "Listing des patients", link: "/patient-listing/"}, {name: "Liste des patients", link: ""}]
        break;

    case `/patient-listing/month-rdv-listing/` :
        items = [{name: "Accueil", link: "/"}, {name: "Liste des relances", link: "/patient-listing/"}, {name: "Liste des RDV du mois", link: ""}]
        break;

    case `/patient-listing/lost-rdv/` :
        items = [{name: "Accueil", link: "/"}, {name: "Liste des relances", link: "/patient-listing/"}, {name: "Liste des patients perdus de vues", link: ""}]
        break;

    case `/patient-listing/missed-rdv/` :
        items = [{name: "Accueil", link: "/"}, {name: "Liste des relances", link: "/patient-listing/"}, {name: "Liste des RDV manqués", link: ""}]
        break;

    case `/patient-listing/lost-patient/` :
        items = [{name: "Accueil", link: "/"}, {name: "Liste des relances", link: "/patient-listing/"}, {name: "Liste patient perdus de vues", link: ""}]
        break;

    // END

    case "/profile/":
        items = [{name: "Accueil", link: "/"}, {name: "Profile utilisateur", link: ""}]
        break;
    
    case "/site-list/":
        items = [{name: "Accueil", link: "/"}, {name: "Liste des sites", link: ""}]
        break; 
            
    case "/site-list/create/":
        items = [{name: "Accueil", link: "/"}, {name: "Liste des sites", link: "/site-list/"}, {name: "Création de site", link: ""}]
        break;
            
    case /\/site-list\/edit\/\d/:
        items = [{name: "Accueil", link: "/"}, {name: "Liste des sites", link: "/site-list/"}, {name: "Modification du site", link: ""}]
        break;

    // Relance Patient Link
    case "/relance/list-relance/" :
        items = [{name: "Accueil", link: "/"}, {name: "Liste des relances", link: ""}]
        break;

    case "/relance/add-relance/" :
        items = [{name: "Accueil", link: "/"}, {name: "Liste des relances", link: "/relance/list-relance/"}, {name: "Ajout de relance", link: ""}]
        break;

    case `/relance/edit-relance/${/[a-z,A-Z,)-9]{8}/}` :
        items = [{name: "Accueil", link: "/"}, {name: "Liste des relances", link: "/relance/list-relance/"}, {name: "Modification de relance", link: ""}]
        break;
    
    case `/relance/list-site-relance/` :
        items = [{name: "Accueil", link: "/"}, {name: "Liste des relances", link: ""}]
        break;

    default:
        items = []
        break;
}


if (domContainer) ReactDOM.render(<Breadcrumb items={items}/>, domContainer);
if (cardBox) ReactDOM.render(<Card />, cardBox);
