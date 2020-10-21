package burgers;



public interface InterfaceBurguer {
	
	default void makeRecipe() {
		System.out.println("Making Default CheeseBurger recipe!!!");
	}
	

}
