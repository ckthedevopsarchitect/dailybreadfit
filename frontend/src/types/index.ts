/**
 * TypeScript types and interfaces
 */

export interface User {
  user_id: string;
  email: string;
  name: string;
  role: string;
  is_active: boolean;
  created_at: number;
}

export interface UserProfile {
  user_id: string;
  fitness_goal: 'weight_loss' | 'weight_gain' | 'maintenance' | 'muscle_gain';
  dietary_preferences: string[];
  allergies: string[];
  height?: number;
  weight?: number;
  age?: number;
  gender?: 'male' | 'female' | 'other';
  activity_level: 'sedentary' | 'light' | 'moderate' | 'active' | 'very_active';
  created_at: number;
}

export interface Recipe {
  recipe_id: string;
  name: string;
  description: string;
  category: string;
  ingredients: string[];
  instructions: string[];
  prep_time: number;
  cook_time: number;
  servings: number;
  nutrition: NutritionInfo;
  image_url?: string;
  difficulty: 'easy' | 'medium' | 'hard';
  tags: string[];
  created_at: number;
}

export interface NutritionInfo {
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  fiber?: number;
  sugar?: number;
}

export interface DailyTip {
  tip_id: string;
  title: string;
  content: string;
  category: string;
  image_url?: string;
  created_at: number;
}

export interface MealRecommendation {
  name: string;
  description: string;
  ingredients: string[];
  nutrition: NutritionInfo;
  prep_time: string;
  difficulty: string;
}

export interface MealPlan {
  plan_id: string;
  user_id: string;
  date: string;
  meals: {
    breakfast?: MealRecommendation;
    lunch?: MealRecommendation;
    dinner?: MealRecommendation;
    snacks?: MealRecommendation[];
  };
  total_nutrition: NutritionInfo;
  created_at: number;
}

export interface Order {
  order_id: string;
  user_id: string;
  items: OrderItem[];
  total_amount: number;
  status: 'pending' | 'confirmed' | 'preparing' | 'delivered' | 'cancelled';
  delivery_address: Address;
  payment_method: string;
  payment_status: 'pending' | 'paid' | 'failed';
  created_at: number;
  updated_at: number;
}

export interface OrderItem {
  meal_name: string;
  quantity: number;
  price: number;
  meal_type: 'breakfast' | 'lunch' | 'dinner';
  customizations?: string[];
}

export interface Address {
  street: string;
  city: string;
  state: string;
  zip_code: string;
  country: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user_id: string;
  email: string;
  name: string;
}
