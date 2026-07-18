import { initializeApp } from 'https://www.gstatic.com/firebasejs/12.16.0/firebase-app.js';
import { getFirestore, collection, addDoc, serverTimestamp }
  from 'https://www.gstatic.com/firebasejs/12.16.0/firebase-firestore.js';
import { firebaseConfig } from './firebase-config.js';

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

window.submitLaunchListSignup = async function (data) {
  await addDoc(collection(db, 'launchListSignups'), {
    fullName: data.fullName,
    phone: data.phone,
    place: data.place,
    submittedAt: serverTimestamp()
  });
};
