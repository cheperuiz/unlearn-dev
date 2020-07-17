package burgers;

import java.util.List;

public abstract class  AbstractBurger {

	protected List<String> ingredients;

	public abstract void makeRecipe();
	
	public List<String> getIngredients() {
		return ingredients;
	}

	public void setIngredients(List<String> ingredients) {
		this.ingredients = ingredients;
	}

}
