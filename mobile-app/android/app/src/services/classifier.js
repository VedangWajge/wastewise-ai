export const classifyWaste = async (imageUri) => {
  // Simulate AI processing delay
  await new Promise((r) => setTimeout(r, 2000));

  const categories = ['eWaste', 'Plastic', 'Metal', 'Organic', 'Paper'];
  const random = Math.floor(Math.random() * categories.length);

  return {
    category: categories[random],
    confidence: Math.random(),
  };
};
