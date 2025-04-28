import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { 
  HiOutlineCalendar, 
  HiOutlineScale, 
  HiOutlineCake,
  HiOutlineChartPie,
  HiOutlineDocumentDownload, 
  HiOutlineInformationCircle, 
  HiOutlineCode, 
  HiOutlineClipboardCopy, 
  HiOutlineCheck,
  HiOutlineX
} from 'react-icons/hi';
import { jsPDF } from 'jspdf';
import 'jspdf-autotable';

// Add a dish image mapping
const DISH_IMAGES = {
  "Paneer Butter Masala": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=800&q=80",
  "Dal Makhani": "https://images.unsplash.com/photo-1617692855027-33b14f061079?w=800&q=80",
  "Chole Bhature": "https://images.unsplash.com/photo-1626777552726-4dca0447bcd4?w=800&q=80",
  "Butter Chicken": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=800&q=80",
  "Masala Dosa": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=800&q=80",
  "Idli": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=800&q=80",
  "Aloo Gobi": "https://images.unsplash.com/photo-1645177628172-a94a6177d2ba?w=800&q=80",
  "Biryani": "https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=800&q=80",
};

const DEFAULT_IMAGE_URL = "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800&q=80";

const PLACEHOLDER_IMAGE_URL = "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=600&q=80";

const ResultCard = styled.div`
  background: var(--card-bg);
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
`;

const ResultHeader = styled.div`
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  padding: 2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
`;

const DishTitle = styled.h2`
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 0.5rem;
`;

const DishType = styled.div`
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 0.35rem 1rem;
  border-radius: var(--border-radius-full);
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 1rem;
`;

const HeaderPattern = styled.div`
  position: absolute;
  bottom: -10px;
  left: 0;
  right: 0;
  height: 40px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 320'%3E%3Cpath fill='white' fill-opacity='1' d='M0,96L60,112C120,128,240,160,360,165.3C480,171,600,149,720,138.7C840,128,960,128,1080,144C1200,160,1320,192,1380,208L1440,224L1440,320L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z'%3E%3C/path%3E%3C/svg%3E");
  background-size: cover;
  z-index: 1;
`;

const NutritionGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  padding: 1.5rem;
  
  @media (min-width: 640px) {
    grid-template-columns: repeat(3, 1fr);
  }
  
  @media (min-width: 768px) {
    padding: 2rem;
    grid-template-columns: repeat(5, 1fr);
  }
`;

const NutrientCard = styled.div`
  background: ${props => `rgba(${props.bgColor}, 0.1)`};
  border-radius: var(--border-radius);
  padding: 1rem;
  text-align: center;
  transition: var(--transition);
  
  &:hover {
    transform: translateY(-5px);
  }
`;

const NutrientIcon = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: ${props => `rgb(${props.bgColor})`};
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 0.75rem;
`;

const NutrientValue = styled.div`
  font-size: 1.5rem;
  font-weight: 600;
  color: ${props => `rgb(${props.color})`};
  margin-bottom: 0.25rem;
`;

const NutrientLabel = styled.div`
  font-size: 0.75rem;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
`;

const ServingSizeNote = styled.div`
  background: var(--light-bg);
  margin: 0 1.5rem 1.5rem;
  padding: 0.75rem 1rem;
  border-radius: var(--border-radius);
  font-size: 0.875rem;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  
  @media (min-width: 768px) {
    margin: 0 2rem 2rem;
  }
`;

const IngredientsSection = styled.div`
  padding: 0 1.5rem 1.5rem;
  
  @media (min-width: 768px) {
    padding: 0 2rem 2rem;
  }
`;

const SectionTitle = styled.h3`
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const IngredientsGrid = styled.div`
  display: grid;
  gap: 0.75rem;
  
  @media (min-width: 640px) {
    grid-template-columns: repeat(2, 1fr);
  }
`;

const IngredientItem = styled.div`
  background: var(--light-bg);
  border-radius: var(--border-radius);
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  
  ${props => props.excluded && `
    background: rgba(239, 68, 68, 0.05);
    border: 1px dashed rgba(239, 68, 68, 0.3);
  `}
`;

const IngredientHeader = styled.div`
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
`;

const IngredientName = styled.span`
  font-weight: 500;
  color: var(--text-color);
`;

const IngredientQuantity = styled.span`
  color: var(--text-secondary);
  white-space: nowrap;
  font-size: 0.75rem;
  background: rgba(0, 0, 0, 0.05);
  padding: 0.2rem 0.5rem;
  border-radius: var(--border-radius-full);
`;

const MatchInfoRow = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const MatchInfo = styled.span`
  font-size: 0.75rem;
  color: ${props => props.excluded ? 'var(--error-color)' : 'var(--secondary-color)'};
`;

const ConfidenceBar = styled.div`
  height: 4px;
  width: 100%;
  background: #eee;
  border-radius: 2px;
  position: relative;
  overflow: hidden;
  margin-top: 0.5rem;
`;

const ConfidenceLevel = styled.div`
  position: absolute;
  height: 100%;
  width: ${props => props.level}%;
  background: ${props => 
    props.level > 90 ? 'var(--success-color)' : 
    props.level > 70 ? 'var(--warning-color)' : 
    'var(--error-color)'};
  left: 0;
  top: 0;
`;

const ButtonsContainer = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
  padding: 0 1.5rem 1.5rem;
  
  @media (min-width: 640px) {
    grid-template-columns: repeat(2, 1fr);
  }
  
  @media (min-width: 768px) {
    padding: 0 2rem 2rem;
  }
`;

const JsonViewerContainer = styled.div`
  margin: 0 1.5rem 1.5rem;
  border-radius: var(--border-radius);
  overflow: hidden;
  border: 1px solid #e5e7eb;
  
  @media (min-width: 768px) {
    margin: 0 2rem 2rem;
  }
`;

const JsonViewerHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8f9fa;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e5e7eb;
`;

const JsonViewerTitle = styled.div`
  font-weight: 500;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
`;

const CopyButton = styled.button`
  background: none;
  border: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--primary-color);
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  cursor: pointer;
  
  &:hover {
    color: var(--primary-dark);
    background: none;
    transform: none;
  }
`;

const JsonContent = styled.pre`
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 1rem;
  overflow: auto;
  margin: 0;
  font-size: 0.875rem;
  max-height: 300px;
`;

const ErrorContainer = styled.div`
  padding: 2rem;
  text-align: center;
  color: var(--error-color);
`;

const ErrorIcon = styled.div`
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.1);
  color: var(--error-color);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  font-size: 1.5rem;
`;

const DishImage = styled.div`
  width: 100%;
  height: 180px;
  margin-bottom: -40px;
  margin-top: 1rem;
  position: relative;
  overflow: hidden;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 2;
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
  }
  
  &:hover img {
    transform: scale(1.05);
  }
`;

const DishImageOverlay = styled.div`
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
  padding: 20px 15px 15px;
  
  h3 {
    color: white;
    margin: 0;
    font-size: 1.25rem;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
  }
  
  span {
    color: rgba(255, 255, 255, 0.8);
    font-size: 0.875rem;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    margin-top: 5px;
  }
`;

function NutritionResult({ result }) {
  const [showJson, setShowJson] = useState(false);
  const [copied, setCopied] = useState(false);
  const [dishImage, setDishImage] = useState(DEFAULT_IMAGE_URL);
  
  useEffect(() => {
    // Set the dish image based on the dish name
    if (result && result.dish_name) {
      // Try exact match first
      const exactMatch = DISH_IMAGES[result.dish_name];
      if (exactMatch) {
        setDishImage(exactMatch);
        return;
      }
      
      // Try partial match
      const dishNameLower = result.dish_name.toLowerCase();
      for (const [key, url] of Object.entries(DISH_IMAGES)) {
        if (dishNameLower.includes(key.toLowerCase()) || key.toLowerCase().includes(dishNameLower)) {
          setDishImage(url);
          return;
        }
      }
      
      // Set default image based on dish type
      if (result.dish_type) {
        switch(result.dish_type) {
          case "South Indian":
            setDishImage("https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=800&q=80");
            break;
          case "Dal":
            setDishImage("https://images.unsplash.com/photo-1617692855027-33b14f061079?w=800&q=80");
            break;
          case "Wet Sabzi":
            setDishImage("https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=800&q=80");
            break;
          default:
            setDishImage(DEFAULT_IMAGE_URL);
        }
      }
    }
  }, [result]);

  // Handle error cases
  if (result.error) {
    return (
      <ResultCard>
        <ErrorContainer>
          <ErrorIcon>
            <HiOutlineX />
          </ErrorIcon>
          <h3>Error: {result.error}</h3>
          <p>Dish not recognized. Try another Indian dish name.</p>
        </ErrorContainer>
      </ResultCard>
    );
  }

  // Extract the nutrition key (it's dynamically named based on serving size)
  const nutritionKey = Object.keys(result).find(key => key.startsWith('estimated_nutrition_per_'));
  const nutritionData = nutritionKey ? result[nutritionKey] : null;
  
  // Extract serving size from the key name
  const servingSizeMatch = nutritionKey?.match(/estimated_nutrition_per_(.+)/);
  const servingSize = servingSizeMatch ? servingSizeMatch[1].replace('_', ' ') : 'standard serving';

  if (!nutritionData) {
    return (
      <ResultCard>
        <ErrorContainer>
          <ErrorIcon>
            <HiOutlineX />
          </ErrorIcon>
          <h3>No Data Found</h3>
          <p>No nutritional data available for this dish.</p>
        </ErrorContainer>
      </ResultCard>
    );
  }
  
  // Generate confidence levels for matching
  const generateConfidence = (matchedString) => {
    if (!matchedString) return 0;
    if (matchedString === "not found") return 30;
    if (matchedString.includes("partial")) return 75;
    if (matchedString.includes("approximate")) return 85;
    return 95;
  };
  
  // Check if ingredient should be excluded from calculation
  const isExcluded = (quantity) => {
    return quantity.includes('to taste') || quantity.includes('for garnish') || quantity.includes('as needed');
  };
  
  // Download PDF report
  const handleDownloadPDF = () => {
    const doc = new jsPDF();
    
    // Add title
    doc.setFontSize(18);
    doc.setTextColor(44, 62, 80);
    doc.text(`Nutrition Report: ${result.dish_name}`, 15, 20);
    
    // Add dish type
    doc.setFontSize(12);
    doc.setTextColor(52, 73, 94);
    doc.text(`Dish Type: ${result.dish_type}`, 15, 30);
    
    // Serving size note
    doc.text(`Nutrition per ${servingSize}:`, 15, 40);
    
    // Nutrients table
    const nutrientsData = [
      ['Nutrient', 'Amount'],
      ['Calories', `${nutritionData.calories.toFixed(1)} kcal`],
      ['Protein', `${nutritionData.protein.toFixed(1)} g`],
      ['Carbs', `${nutritionData.carbs.toFixed(1)} g`],
      ['Fat', `${nutritionData.fat.toFixed(1)} g`],
      ['Fiber', `${nutritionData.fiber.toFixed(1)} g`]
    ];
    
    doc.autoTable({
      startY: 45,
      head: [nutrientsData[0]],
      body: nutrientsData.slice(1),
      theme: 'grid',
      headStyles: { fillColor: [79, 70, 229] }
    });
    
    // Ingredients table
    const ingredientsData = [
      ['Ingredient', 'Quantity', 'Matched To'],
      ...result.ingredients_used.map(item => [
        item.ingredient,
        item.quantity,
        isExcluded(item.quantity) 
          ? 'Excluded from nutrition calculation'
          : item.matched_to
      ])
    ];
    
    doc.autoTable({
      startY: doc.lastAutoTable.finalY + 15,
      head: [ingredientsData[0]],
      body: ingredientsData.slice(1),
      theme: 'grid',
      headStyles: { fillColor: [16, 185, 129] }
    });
    
    // Add note
    doc.setFontSize(10);
    doc.setTextColor(100, 100, 100);
    const now = new Date();
    doc.text(`Generated on: ${now.toLocaleDateString()} at ${now.toLocaleTimeString()}`, 15, doc.lastAutoTable.finalY + 15);
    doc.text("NutriCalc AI - Powered by IFCT database", 15, doc.lastAutoTable.finalY + 22);
    
    doc.save(`${result.dish_name.replace(/ /g, '_')}_nutrition.pdf`);
  };

  // Generate clean JSON for export
  const generateCleanJson = () => {
    const cleanData = {
      dish_name: result.dish_name,
      dish_type: result.dish_type,
      [nutritionKey]: nutritionData,
      ingredients_used: result.ingredients_used
    };
    
    return JSON.stringify(cleanData, null, 2);
  };
  
  // Download JSON file
  const handleExportJson = () => {
    const jsonData = generateCleanJson();
    const blob = new Blob([jsonData], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${result.dish_name.replace(/ /g, '_').toLowerCase()}_nutrition.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };
  
  // Copy JSON to clipboard
  const handleCopyJson = () => {
    navigator.clipboard.writeText(generateCleanJson());
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  
  // Toggle JSON viewer
  const toggleJsonView = () => {
    setShowJson(!showJson);
  };

  return (
    <ResultCard>
      <ResultHeader>
        <DishTitle>{result.dish_name}</DishTitle>
        <DishType>
          <HiOutlineChartPie size={14} />
          {result.dish_type}
        </DishType>
        
        <DishImage>
          <img src={dishImage} alt={result.dish_name} />
          <DishImageOverlay>
            <h3>{result.dish_name}</h3>
            <span><HiOutlineChartPie size={14} /> {result.dish_type}</span>
          </DishImageOverlay>
        </DishImage>
        
        <HeaderPattern />
      </ResultHeader>
      
      <NutritionGrid>
        <NutrientCard bgColor="239, 68, 68">
          <NutrientIcon bgColor="239, 68, 68">
            <HiOutlineCalendar size={18} />
          </NutrientIcon>
          <NutrientValue color="239, 68, 68">{nutritionData.calories.toFixed(1)}</NutrientValue>
          <NutrientLabel>Calories</NutrientLabel>
        </NutrientCard>
        
        <NutrientCard bgColor="16, 185, 129">
          <NutrientIcon bgColor="16, 185, 129">
            <HiOutlineScale size={18} />
          </NutrientIcon>
          <NutrientValue color="16, 185, 129">{nutritionData.protein.toFixed(1)}g</NutrientValue>
          <NutrientLabel>Protein</NutrientLabel>
        </NutrientCard>
        
        <NutrientCard bgColor="59, 130, 246">
          <NutrientIcon bgColor="59, 130, 246">
            <HiOutlineCake size={18} />
          </NutrientIcon>
          <NutrientValue color="59, 130, 246">{nutritionData.carbs.toFixed(1)}g</NutrientValue>
          <NutrientLabel>Carbs</NutrientLabel>
        </NutrientCard>
        
        <NutrientCard bgColor="245, 158, 11">
          <NutrientIcon bgColor="245, 158, 11">
            <HiOutlineScale size={18} />
          </NutrientIcon>
          <NutrientValue color="245, 158, 11">{nutritionData.fat.toFixed(1)}g</NutrientValue>
          <NutrientLabel>Fat</NutrientLabel>
        </NutrientCard>
        
        <NutrientCard bgColor="139, 92, 246">
          <NutrientIcon bgColor="139, 92, 246">
            <HiOutlineChartPie size={18} />
          </NutrientIcon>
          <NutrientValue color="139, 92, 246">{nutritionData.fiber?.toFixed(1) || 0}g</NutrientValue>
          <NutrientLabel>Fiber</NutrientLabel>
        </NutrientCard>
      </NutritionGrid>

      <ServingSizeNote>
        <HiOutlineInformationCircle size={16} />
        <span>
          Nutrition values shown per {servingSize}
        </span>
      </ServingSizeNote>

      {result.ingredients_used && result.ingredients_used.length > 0 && (
        <IngredientsSection>
          <SectionTitle>
            <HiOutlineChartPie size={16} />
            Ingredients
          </SectionTitle>
          
          <IngredientsGrid>
            {result.ingredients_used.map((ingredient, index) => {
              const excluded = isExcluded(ingredient.quantity);
              const confidence = generateConfidence(ingredient.matched_to);
              
              return (
                <IngredientItem key={index} excluded={excluded}>
                  <IngredientHeader>
                    <IngredientName>{ingredient.ingredient}</IngredientName>
                    <IngredientQuantity>{ingredient.quantity}</IngredientQuantity>
                  </IngredientHeader>
                  
                  <MatchInfoRow>
                    <MatchInfo excluded={excluded}>
                      {excluded 
                        ? 'Excluded from calculation' 
                        : ingredient.matched_to || 'Not found in database'}
                    </MatchInfo>
                  </MatchInfoRow>
                  
                  {!excluded && (
                    <ConfidenceBar>
                      <ConfidenceLevel level={confidence} />
                    </ConfidenceBar>
                  )}
                </IngredientItem>
              );
            })}
          </IngredientsGrid>
        </IngredientsSection>
      )}
      
      {showJson && (
        <JsonViewerContainer>
          <JsonViewerHeader>
            <JsonViewerTitle>
              <HiOutlineCode size={16} />
              JSON Data
            </JsonViewerTitle>
            <CopyButton onClick={handleCopyJson}>
              {copied ? <HiOutlineCheck size={14} /> : <HiOutlineClipboardCopy size={14} />}
              {copied ? "Copied!" : "Copy"}
            </CopyButton>
          </JsonViewerHeader>
          <JsonContent>
            {generateCleanJson()}
          </JsonContent>
        </JsonViewerContainer>
      )}
      
      <ButtonsContainer>
        <button className="secondary" onClick={toggleJsonView}>
          <HiOutlineCode size={18} />
          {showJson ? "Hide JSON Data" : "Show JSON Data"}
        </button>
        <button className="success" onClick={handleDownloadPDF}>
          <HiOutlineDocumentDownload size={18} />
          Download PDF Report
        </button>
      </ButtonsContainer>
    </ResultCard>
  );
}

export default NutritionResult;
