const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const  cors = require('cors')
const app = express()
const port = 3030;
// app.use('/api/reviews', require('./routes/reviews'));

app.use(cors())
app.use(require('body-parser').urlencoded({ extended: false }));
// updating two route down here 
// const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
// const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

const reviews_data = JSON.parse(fs.readFileSync("./data/reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("./data/dealerships.json", 'utf8'));

mongoose.connect("mongodb://mongo_db:27017/",{'dbName':'dealershipsDB'});


// added by chat gpt for better performance
// While this is mostly correct, it’s missing important options for proper connection handling and could be causing connection instability issues.
// --------------------------------suggestion+++++++++++++++++++++++
// const mongoose = require('mongoose');

// mongoose.connect("mongodb://mongo_db:27017/dealershipsDB", {
//   useNewUrlParser: true,         // Use the new URL parser
//   useUnifiedTopology: true,      // Use the new server discovery and monitoring engine
//   serverSelectionTimeoutMS: 5000,  // Timeout after 5 seconds if MongoDB is unreachable
// })
//   .then(() => console.log("✅ MongoDB connected successfully"))
//   .catch(err => console.error("❌ Error connecting to MongoDB:", err));

// ===============================+++++++++++++++++++++++++++++++++++
const Reviews = require('./review');

const Dealerships = require('./dealership');
//++++++++++++++++++++++suggestion++++++++++++++++++++++++++++++++
// try {
//   // Use await for proper seeding
//   await Reviews.deleteMany({});
//   await Reviews.insertMany(reviews_data['reviews']);

//   await Dealerships.deleteMany({});
//   await Dealerships.insertMany(dealerships_data['dealerships']);

//   console.log("Database seeded successfully!");
// } catch (error) {
//   console.error("Error seeding the database:", error);
// }
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
try {
  Reviews.deleteMany({}).then(()=>{
    Reviews.insertMany(reviews_data['reviews']);
  });
  Dealerships.deleteMany({}).then(()=>{
    Dealerships.insertMany(dealerships_data['dealerships']);
  });
  
} catch (error) {
  res.status(500).json({ error: 'Error fetching documents' });
}


// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Mongoose API")
});

// Express route to fetch all reviews
// can get this only not the rest.
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    // adding this line hopefully works
    console.error( "Error fetching reviews:", error);
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({ dealership: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
//Write your code here
console.log("Fetching all dealers..."); // Log added chatgpt
try{
  // const documents = await Dealers.find();
  const documents = await Dealerships.find(); //why?
  console.log("Fetched dealers:", documents); // Log the result chatgpt
  res.json(documents);
}catch(error) {
  console .error("Error fetching dealers:", error);//why adding this line 
  res.status(500).json({ error: 'Error fetching documents' })
}
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
//Write your code here
try {
  // const documents = await Reviews.find({dealership: req.params.id});example
  // const documents = await Dealers.find({dealership: req.params.state});
  const documents = await Dealerships.find({state: req.params.state});

  if (documents.length === 0) {
    return res.status(404).json({ error: "No dealers found in this state"});
  }
  res.json(documents);
} catch(error) {
  console.error("Error fetching dealers by state:", error );// adding this line why?
  res.status(500).json({ error: 'Error fetching documents' });
}
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
//Write your code here
try{
  // Blew the code not Correct I should use "findById" 
  // because we want one thing in here so we use "findById"
//   const documents = await Dealers.find({dealership: req.params.id});
//   res.json(documents)
// }catch(error) {  // this is not enough should add more catch error.
//   res.status(500).json({ error: 'Error fetching documents' })
// Modify the endpoint to use findOne with a filter on a numeric field

//const document = await Dealerships.findById(req.params.id);
const document = await Dealerships.findOne({ id: req.params.id });


if (!document) {
  return res.status(404).json({ error: "Dealer not found"});
  }

  res.json(document)
} catch (error) {
  console.error("Error fetching dealer by ID:", error);

  // More specific error handling for invalid ObjectId
  if (error.kind === 'ObjectId') {
    return res.status(400).json({ error: "Invalid Dealer ID format "});
  }

  res.status(500).json({ error: "Error fetching dealer"});
}
});
// const PORT = process.env.PORT || 3030; // added by chatgpt why?
// app.listen(PORT, () => console.log(`Server running on port ${PORT}`)); // added by chatgpt why?
//
//google recommendation 
// Express route to fetch all dealerships
// app.get('/dealers', async (req, res) => { //changed route name
//   try {
//     const documents = await Dealers.find();
//     res.json(documents);
//   } catch (error) {
//     console.error("Error fetching all dealers:", error);
//     res.status(500).json({ error: error.message }); // More specific error
//   }
// });

// // Express route to fetch Dealers by a particular state
// app.get('/dealers/state/:state', async (req, res) => { //changed route name
//   try {
//     const documents = await Dealers.find({ state: req.params.state }); // Corrected query
//     res.json(documents);
//   } catch (error) {
//     console.error("Error fetching dealers by state:", error);
//     res.status(500).json({ error: error.message }); // More specific error
//   }
// });

// // Express route to fetch dealer by a particular id
// app.get('/dealer/:id', async (req, res) => { //changed route name
//   try {
//     const document = await Dealers.findById(req.params.id); //findById is better for single document by id.
//     if (!document) {
//       return res.status(404).json({ error: 'Dealer not found' });
//     }
//     res.json(document);
//   } catch (error) {
//     console.error("Error fetching dealer by ID:", error);
//     if(error.kind === 'ObjectId') {
//       return res.status(400).json({error: "Invalid Dealer ID"})
//     }
//     res.status(500).json({ error: error.message }); // More specific error
//   }
// });
// end here 
//
//Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  data = JSON.parse(req.body);
  const documents = await Reviews.find().sort( { id: -1 } )
  let new_id = documents[0]['id']+1

  const review = new Reviews({
		"id": new_id,
		"name": data['name'],
		"dealership": data['dealership'],
		"review": data['review'],
		"purchase": data['purchase'],
		"purchase_date": data['purchase_date'],
		"car_make": data['car_make'],
		"car_model": data['car_model'],
		"car_year": data['car_year'],
	});

  try {
    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
		console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
//     +++++++++++++++++++++++++++++++++=================
//  chat gpt code the above did not fetch all apis
// const express = require('express');
// const mongoose = require('mongoose');
// const cors = require('cors');
// const app = express();
// const port = 3030;

// app.use(cors());
// app.use(require('body-parser').urlencoded({ extended: false }));

// // Connect to MongoDB
// mongoose.connect("mongodb://mongo_db:27017/", { 'dbName': 'dealershipsDB' })
//   .then(() => console.log("MongoDB connected"))
//   .catch(err => console.log("MongoDB connection error:", err));

// // Import your models
// const Reviews = require('./review');
// const Dealerships = require('./dealership');

// // Seed the database (only once or as needed)
// const seedDatabase = async () => {
//   try {
//     await Reviews.deleteMany({});
//     await Dealerships.deleteMany({});

//     // Assuming reviews_data and dealerships_data are already imported from your JSON files or other sources.
//     await Reviews.insertMany(reviews_data['reviews']);
//     await Dealerships.insertMany(dealerships_data['dealerships']);

//     console.log("Database seeded successfully!");
//   } catch (error) {
//     console.error("Error seeding the database:", error);
//   }
// };

// // Seed the database (uncomment the next line to seed once, and comment after first time)
// seedDatabase();

// // Home route
// app.get('/', async (req, res) => {
//   res.send("Welcome to the Mongoose API");
// });

// // Fetch all reviews
// app.get('/fetchReviews', async (req, res) => {
//   try {
//     const documents = await Reviews.find();
//     res.json(documents);
//   } catch (error) {
//     console.error("Error fetching reviews:", error);
//     res.status(500).json({ error: 'Error fetching reviews' });
//   }
// });

// // Fetch reviews by dealership ID
// app.get('/fetchReviews/dealer/:id', async (req, res) => {
//   try {
//     const documents = await Reviews.find({ dealership: req.params.id });
//     res.json(documents);
//   } catch (error) {
//     console.error("Error fetching reviews by dealer:", error);
//     res.status(500).json({ error: 'Error fetching reviews by dealer' });
//   }
// });

// // Fetch all dealerships
// app.get('/fetchDealers', async (req, res) => {
//   try {
//     const documents = await Dealerships.find();
//     res.json(documents);
//   } catch (error) {
//     console.error("Error fetching dealers:", error);
//     res.status(500).json({ error: 'Error fetching dealers' });
//   }
// });

// // Fetch dealerships by state
// app.get('/fetchDealers/:state', async (req, res) => {
//   try {
//     const documents = await Dealerships.find({ state: req.params.state });
//     if (documents.length === 0) {
//       return res.status(404).json({ error: "No dealers found in this state" });
//     }
//     res.json(documents);
//   } catch (error) {
//     console.error("Error fetching dealers by state:", error);
//     res.status(500).json({ error: 'Error fetching dealers by state' });
//   }
// });

// // Fetch a dealer by ID
// app.get('/fetchDealer/:id', async (req, res) => {
//   try {
//     const document = await Dealerships.findById(req.params.id);
//     if (!document) {
//       return res.status(404).json({ error: "Dealer not found" });
//     }
//     res.json(document);
//   } catch (error) {
//     console.error("Error fetching dealer by ID:", error);
//     if (error.kind === 'ObjectId') {
//       return res.status(400).json({ error: "Invalid Dealer ID format" });
//     }
//     res.status(500).json({ error: "Error fetching dealer" });
//   }
// });

// // Insert a review
// app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
//   const data = JSON.parse(req.body);
//   const documents = await Reviews.find().sort({ id: -1 });
//   let new_id = documents[0] ? documents[0]['id'] + 1 : 1;

//   const review = new Reviews({
//     id: new_id,
//     name: data['name'],
//     dealership: data['dealership'],
//     review: data['review'],
//     purchase: data['purchase'],
//     purchase_date: data['purchase_date'],
//     car_make: data['car_make'],
//     car_model: data['car_model'],
//     car_year: data['car_year'],
//   });

//   try {
//     const savedReview = await review.save();
//     res.json(savedReview);
//   } catch (error) {
//     console.log(error);
//     res.status(500).json({ error: 'Error inserting review' });
//   }
// });

// // Start the Express server
// app.listen(port, () => {
//   console.log(`Server is running on http://localhost:${port}`);
// });




//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


// Error Handling:
// The catch block handles errors. The check for error.kind === 'ObjectId' is useful if you're using findById with MongoDB ObjectIDs. Since we're now using findOne with a custom field, this check might be less relevant—but you can keep it for compatibility if your application sometimes uses ObjectIDs.
